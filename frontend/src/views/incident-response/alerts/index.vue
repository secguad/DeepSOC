<template>
  <div class="alerts">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>告警处理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleProcess">批量处理</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 告警概览 -->
      <div class="alert-overview">
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

      <!-- 告警趋势 -->
      <div class="alert-trend">
        <div class="section-title">告警趋势</div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>告警数量趋势</span>
                  <el-select v-model="timeRange" size="small">
                    <el-option label="近7天" value="7" />
                    <el-option label="近30天" value="30" />
                    <el-option label="近90天" value="90" />
                  </el-select>
                </div>
              </template>
              <div class="chart-container" ref="alertCountChartRef"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>告警类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="alertTypeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 告警列表 -->
      <div class="alert-list">
        <div class="section-title">告警列表</div>
        <el-table :data="alertList" style="width: 100%">
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="告警ID" width="120" />
          <el-table-column prop="name" label="告警名称" width="200" />
          <el-table-column prop="type" label="告警类型" width="120">
            <template #default="scope">
              <el-tag :type="getAlertTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="level" label="危险等级" width="100">
            <template #default="scope">
              <el-tag :type="getAlertLevelTag(scope.row.level)">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="source" label="告警来源" width="150" />
          <el-table-column prop="time" label="告警时间" width="180" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getAlertStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleProcess(scope.row)">
                处理
              </el-button>
              <el-button type="warning" link @click="handleIgnore(scope.row)">
                忽略
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 告警详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="告警详情"
      width="800px"
    >
      <div v-if="currentAlert" class="alert-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="告警ID">{{ currentAlert.id }}</el-descriptions-item>
          <el-descriptions-item label="告警名称">{{ currentAlert.name }}</el-descriptions-item>
          <el-descriptions-item label="告警类型">
            <el-tag :type="getAlertTypeTag(currentAlert.type)">
              {{ currentAlert.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="危险等级">
            <el-tag :type="getAlertLevelTag(currentAlert.level)">
              {{ currentAlert.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="告警来源">{{ currentAlert.source }}</el-descriptions-item>
          <el-descriptions-item label="告警时间">{{ currentAlert.time }}</el-descriptions-item>
          <el-descriptions-item label="告警描述" :span="2">{{ currentAlert.description }}</el-descriptions-item>
          <el-descriptions-item label="告警详情" :span="2">{{ currentAlert.details }}</el-descriptions-item>
          <el-descriptions-item label="处理建议" :span="2">{{ currentAlert.suggestion }}</el-descriptions-item>
          <el-descriptions-item label="处理状态">
            <el-tag :type="getAlertStatusTag(currentAlert.status)">
              {{ currentAlert.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="处理时间">{{ currentAlert.processTime || '-' }}</el-descriptions-item>
          <el-descriptions-item label="处理人">{{ currentAlert.processor || '-' }}</el-descriptions-item>
          <el-descriptions-item label="处理结果">{{ currentAlert.result || '-' }}</el-descriptions-item>
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
const alertCountChartRef = ref<HTMLElement | null>(null)
const alertTypeChartRef = ref<HTMLElement | null>(null)

// 定义告警类型接口
interface Alert {
  id: string
  name: string
  type: string
  level: string
  source: string
  time: string
  status: string
  description: string
  details: string
  suggestion: string
  processTime?: string
  processor?: string
  result?: string
}

const overview = ref([
  {
    title: '今日告警',
    value: '25',
    trend: -15
  },
  {
    title: '待处理',
    value: '8',
    trend: -20
  },
  {
    title: '已处理',
    value: '15',
    trend: 10
  },
  {
    title: '已忽略',
    value: '2',
    trend: 0
  }
])

const timeRange = ref('7')

const alertList = ref<Alert[]>([
  {
    id: 'ALERT-2024-001',
    name: '暴力破解攻击',
    type: '攻击告警',
    level: '高危',
    source: 'IDS',
    time: '2024-02-20 10:00:00',
    status: '待处理',
    description: '检测到针对SSH服务的暴力破解攻击',
    details: '源IP: 192.168.1.100\n目标IP: 192.168.1.200\n攻击类型: 暴力破解\n目标端口: 22',
    suggestion: '1. 检查SSH配置\n2. 加强密码策略\n3. 考虑启用双因素认证'
  },
  {
    id: 'ALERT-2024-002',
    name: '异常登录',
    type: '行为告警',
    level: '中危',
    source: 'UEBA',
    time: '2024-02-20 09:30:00',
    status: '已处理',
    description: '检测到用户异常登录行为',
    details: '用户: admin\n登录IP: 192.168.1.150\n登录时间: 2024-02-20 09:30:00\n异常原因: 非工作时间登录',
    suggestion: '1. 验证用户身份\n2. 检查登录设备\n3. 更新登录策略',
    processTime: '2024-02-20 09:35:00',
    processor: '安全管理员',
    result: '已确认是正常登录'
  }
])

const detailVisible = ref(false)
const currentAlert = ref<Alert | null>(null)

const getAlertTypeTag = (type: string): string => {
  switch (type) {
    case '攻击告警':
      return 'danger'
    case '行为告警':
      return 'warning'
    case '系统告警':
      return 'info'
    default:
      return ''
  }
}

const getAlertLevelTag = (level: string): string => {
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

const handleProcess = (row?: Alert) => {
  if (row) {
    ElMessage.success(`开始处理告警：${row.name}`)
  } else {
    ElMessage.success('开始批量处理告警...')
  }
}

const handleExport = () => {
  ElMessage.success('导出报告...')
}

const handleDetail = (row: Alert) => {
  currentAlert.value = row
  detailVisible.value = true
}

const handleIgnore = (row: Alert) => {
  ElMessage.success(`忽略告警：${row.name}`)
}

onMounted(() => {
  // 初始化告警数量趋势图
  const alertCountChart = echarts.init(alertCountChartRef.value!)
  alertCountChart.setOption({
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
        name: '告警数量',
        type: 'line',
        data: [30, 25, 28, 35, 22, 20, 25],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })

  // 初始化告警类型分布图
  const alertTypeChart = echarts.init(alertTypeChartRef.value!)
  alertTypeChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '告警类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 15, name: '攻击告警' },
          { value: 8, name: '行为告警' },
          { value: 2, name: '系统告警' }
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
.alerts {
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

.alert-overview {
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

.alert-trend {
  margin-bottom: 40px;
}

.chart-container {
  height: 300px;
}

.alert-detail {
  padding: 20px;
}
</style> 