<template>
  <div class="cases">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>事件调查</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleCreate">新建事件</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 事件概览 -->
      <div class="case-overview">
        <el-row :gutter="20">
          <el-col :span="6" v-for="(item, index) in overview" :key="index">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">{{ item.title }}</div>
                <div class="overview-value">{{ item.value }}</div>
                <div class="overview-trend">
                  较上期
                  <span :class="item.trend >= 0 ? 'up' : 'down'">
                    {{ Math.abs(item.trend) }}%
                    <el-icon>
                      <component :is="item.trend >= 0 ? 'ArrowUp' : 'ArrowDown'" />
                    </el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 事件趋势 -->
      <div class="case-trend">
        <div class="section-title">事件趋势</div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>事件数量趋势</span>
                  <el-select v-model="timeRange" size="small">
                    <el-option label="近7天" value="7" />
                    <el-option label="近30天" value="30" />
                    <el-option label="近90天" value="90" />
                  </el-select>
                </div>
              </template>
              <div class="chart-container" ref="caseCountChartRef"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>事件类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="caseTypeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 事件列表 -->
      <div class="case-list">
        <div class="section-title">事件列表</div>
        <el-table :data="caseList" style="width: 100%">
          <el-table-column prop="id" label="事件ID" width="120" />
          <el-table-column prop="name" label="事件名称" width="200" />
          <el-table-column prop="type" label="事件类型" width="120">
            <template #default="scope">
              <el-tag :type="getCaseTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="level" label="危险等级" width="100">
            <template #default="scope">
              <el-tag :type="getCaseLevelTag(scope.row.level)">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getCaseStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column prop="updateTime" label="更新时间" width="180" />
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleUpdate(scope.row)">
                更新
              </el-button>
              <el-button type="warning" link @click="handleClose(scope.row)">
                关闭
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 事件详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="事件详情"
      width="800px"
    >
      <div v-if="currentCase" class="case-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="事件ID">{{ currentCase.id }}</el-descriptions-item>
          <el-descriptions-item label="事件名称">{{ currentCase.name }}</el-descriptions-item>
          <el-descriptions-item label="事件类型">
            <el-tag :type="getCaseTypeTag(currentCase.type)">
              {{ currentCase.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="危险等级">
            <el-tag :type="getCaseLevelTag(currentCase.level)">
              {{ currentCase.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getCaseStatusTag(currentCase.status)">
              {{ currentCase.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="负责人">{{ currentCase.owner }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentCase.createTime }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ currentCase.updateTime }}</el-descriptions-item>
          <el-descriptions-item label="事件描述" :span="2">{{ currentCase.description }}</el-descriptions-item>
          <el-descriptions-item label="影响范围" :span="2">{{ currentCase.scope }}</el-descriptions-item>
          <el-descriptions-item label="处理进展" :span="2">
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in currentCase.activities"
                :key="index"
                :timestamp="activity.time"
                :type="activity.type"
              >
                {{ activity.content }}
              </el-timeline-item>
            </el-timeline>
          </el-descriptions-item>
          <el-descriptions-item label="相关告警" :span="2">
            <el-table :data="currentCase.alerts" style="width: 100%">
              <el-table-column prop="id" label="告警ID" width="120" />
              <el-table-column prop="name" label="告警名称" />
              <el-table-column prop="time" label="告警时间" width="180" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getAlertStatusTag(scope.row.status)">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

// 定义图表引用
const caseCountChartRef = ref<HTMLElement | null>(null)
const caseTypeChartRef = ref<HTMLElement | null>(null)

// 定义告警类型接口
interface Alert {
  id: string
  name: string
  time: string
  status: string
}

// 定义活动类型接口
interface Activity {
  time: string
  type: string
  content: string
}

// 定义事件类型接口
interface Case {
  id: string
  name: string
  type: string
  level: string
  status: string
  owner: string
  createTime: string
  updateTime: string
  description: string
  scope: string
  activities: Activity[]
  alerts: Alert[]
}

const overview = ref([
  {
    title: '进行中',
    value: '5',
    trend: -20
  },
  {
    title: '待处理',
    value: '3',
    trend: -25
  },
  {
    title: '已解决',
    value: '12',
    trend: 15
  },
  {
    title: '平均处理时间',
    value: '2.5天',
    trend: -10
  }
])

const timeRange = ref('7')

const caseList = ref<Case[]>([
  {
    id: 'CASE-2024-001',
    name: 'SSH暴力破解事件',
    type: '攻击事件',
    level: '高危',
    status: '进行中',
    owner: '安全管理员',
    createTime: '2024-02-20 10:00:00',
    updateTime: '2024-02-20 11:30:00',
    description: '检测到针对SSH服务的暴力破解攻击，需要及时处理。',
    scope: '影响范围：所有SSH服务器\n涉及资产：10台服务器\n受影响用户：5个',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'primary',
        content: '事件创建'
      },
      {
        time: '2024-02-20 10:30:00',
        type: 'success',
        content: '已确认攻击来源IP'
      },
      {
        time: '2024-02-20 11:00:00',
        type: 'warning',
        content: '正在分析攻击特征'
      }
    ],
    alerts: [
      {
        id: 'ALERT-2024-001',
        name: '暴力破解攻击',
        time: '2024-02-20 10:00:00',
        status: '已处理'
      }
    ]
  },
  {
    id: 'CASE-2024-002',
    name: '异常登录事件',
    type: '安全事件',
    level: '中危',
    status: '已解决',
    owner: '安全管理员',
    createTime: '2024-02-20 09:30:00',
    updateTime: '2024-02-20 10:30:00',
    description: '检测到用户异常登录行为，需要核实。',
    scope: '影响范围：用户登录系统\n涉及资产：1个\n受影响用户：1个',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'primary',
        content: '事件创建'
      },
      {
        time: '2024-02-20 10:00:00',
        type: 'success',
        content: '已确认是正常登录'
      },
      {
        time: '2024-02-20 10:30:00',
        type: 'success',
        content: '事件已关闭'
      }
    ],
    alerts: [
      {
        id: 'ALERT-2024-002',
        name: '异常登录',
        time: '2024-02-20 09:30:00',
        status: '已处理'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentCase = ref<Case | null>(null)

const getCaseTypeTag = (type: string): string => {
  switch (type) {
    case '攻击事件':
      return 'danger'
    case '安全事件':
      return 'warning'
    case '系统事件':
      return 'info'
    default:
      return ''
  }
}

const getCaseLevelTag = (level: string): string => {
  switch (level) {
    case '高危':
      return 'danger'
    case '中危':
      return 'warning'
    case '低危':
      return 'info'
    default:
      return ''
  }
}

const getCaseStatusTag = (status: string): string => {
  switch (status) {
    case '进行中':
      return 'primary'
    case '待处理':
      return 'warning'
    case '已解决':
      return 'success'
    case '已关闭':
      return 'info'
    default:
      return ''
  }
}

const getAlertStatusTag = (status: string): string => {
  switch (status) {
    case '待处理':
      return 'warning'
    case '处理中':
      return 'primary'
    case '已处理':
      return 'success'
    case '已忽略':
      return 'info'
    default:
      return ''
  }
}

const handleCreate = () => {
  ElMessage.success('创建新事件...')
}

const handleExport = () => {
  ElMessage.success('导出报告...')
}

const handleDetail = (row: Case) => {
  currentCase.value = row
  detailVisible.value = true
}

const handleUpdate = (row: Case) => {
  ElMessage.success(`更新事件：${row.name}`)
}

const handleClose = (row: Case) => {
  ElMessage.success(`关闭事件：${row.name}`)
}

onMounted(() => {
  // 初始化事件数量趋势图
  const caseCountChart = echarts.init(caseCountChartRef.value!)
  caseCountChart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['2-14', '2-15', '2-16', '2-17', '2-18', '2-19', '2-20']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '事件数量',
        type: 'line',
        data: [5, 3, 4, 6, 2, 3, 5],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })

  // 初始化事件类型分布图
  const caseTypeChart = echarts.init(caseTypeChartRef.value!)
  caseTypeChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '事件类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 8, name: '攻击事件' },
          { value: 5, name: '安全事件' },
          { value: 3, name: '系统事件' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  })
})
</script>

<style scoped>
.cases {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 20px;
}

.case-overview {
  margin-bottom: 40px;
}

.overview-item {
  text-align: center;
}

.overview-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.overview-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.overview-trend {
  font-size: 14px;
  color: #909399;
}

.up {
  color: #67c23a;
}

.down {
  color: #f56c6c;
}

.case-trend {
  margin-bottom: 40px;
}

.chart-container {
  height: 300px;
}

.case-detail {
  padding: 20px;
}
</style> 