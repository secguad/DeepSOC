<template>
  <div class="anomaly">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>异常检测</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleDetect">开始检测</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 异常概览 -->
      <div class="anomaly-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">今日异常</div>
                <div class="overview-value">45</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    12
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">高风险异常</div>
                <div class="overview-value">8</div>
                <div class="overview-trend">
                  较昨日
                  <span class="down">
                    3
                    <el-icon><ArrowDown /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">检测规则</div>
                <div class="overview-value">25</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    2
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 异常趋势 -->
      <div class="anomaly-trend">
        <div class="section-title">异常趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>异常检测趋势</span>
                  <el-select v-model="timeRange" size="small">
                    <el-option label="近7天" value="7" />
                    <el-option label="近30天" value="30" />
                    <el-option label="近90天" value="90" />
                  </el-select>
                </div>
              </template>
              <div class="chart-container" ref="trendChartRef"></div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>异常类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="typeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 异常列表 -->
      <div class="anomaly-list">
        <div class="section-title">异常列表</div>
        <el-table :data="anomalyList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="name" label="异常名称" />
          <el-table-column prop="type" label="异常类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="level" label="风险等级" width="100">
            <template #default="scope">
              <el-tag :type="getLevelTag(scope.row.level)">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="time" label="发现时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleInvestigate(scope.row)">
                调查
              </el-button>
              <el-button type="warning" link @click="handleBlock(scope.row)">
                阻断
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="异常详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="异常名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="异常类型">
            <el-tag :type="getTypeTag(currentItem.type)">
              {{ currentItem.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag :type="getLevelTag(currentItem.level)">
              {{ currentItem.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="发现时间">{{ currentItem.time }}</el-descriptions-item>
          <el-descriptions-item label="检测规则">{{ currentItem.rule }}</el-descriptions-item>
          <el-descriptions-item label="异常描述" :span="2">{{ currentItem.description }}</el-descriptions-item>
          <el-descriptions-item label="影响范围" :span="2">{{ currentItem.scope }}</el-descriptions-item>
          <el-descriptions-item label="处理记录" :span="2">
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in currentItem.activities"
                :key="index"
                :timestamp="activity.time"
                :type="activity.type"
              >
                {{ activity.content }}
              </el-timeline-item>
            </el-timeline>
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
const trendChartRef = ref<HTMLElement | null>(null)
const typeChartRef = ref<HTMLElement | null>(null)

const timeRange = ref('7')

// 异常列表数据
const anomalyList = ref([
  {
    id: 'ANOMALY-2024-001',
    name: '异常登录行为',
    type: '账户安全',
    level: '高风险',
    time: '2024-02-20 10:00:00',
    rule: '异地登录检测',
    description: '检测到用户从异常IP地址登录系统',
    scope: '影响账户安全，可能导致未授权访问',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'danger',
        content: '发现异常登录行为'
      },
      {
        time: '2024-02-20 10:05:00',
        type: 'warning',
        content: '发送安全通知'
      }
    ]
  },
  {
    id: 'ANOMALY-2024-002',
    name: '数据访问异常',
    type: '数据安全',
    level: '中风险',
    time: '2024-02-20 09:30:00',
    rule: '敏感数据访问检测',
    description: '检测到异常的数据访问模式',
    scope: '影响数据安全，可能导致数据泄露',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'warning',
        content: '发现数据访问异常'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '账户安全':
      return 'danger'
    case '数据安全':
      return 'warning'
    case '系统安全':
      return 'info'
    default:
      return ''
  }
}

const getLevelTag = (level: string): string => {
  switch (level) {
    case '高风险':
      return 'danger'
    case '中风险':
      return 'warning'
    case '低风险':
      return 'info'
    default:
      return ''
  }
}

const handleDetect = (row: any) => {
  ElMessage.success(`开始检测异常: ${row.name}`)
}

const handleExport = () => {
  ElMessage.success('导出异常报告...')
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleInvestigate = (row: any) => {
  ElMessage.success(`开始调查异常: ${row.name}`)
}

const handleBlock = (row: any) => {
  ElMessage.success(`开始阻断异常: ${row.name}`)
}

onMounted(() => {
  // 初始化趋势图
  const trendChart = echarts.init(trendChartRef.value!)
  trendChart.setOption({
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
        name: '异常数量',
        type: 'line',
        data: [35, 42, 38, 45, 40, 43, 45],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })

  // 初始化类型分布图
  const typeChart = echarts.init(typeChartRef.value!)
  typeChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '异常类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '账户安全' },
          { value: 30, name: '数据安全' },
          { value: 20, name: '系统安全' },
          { value: 10, name: '其他' }
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
.anomaly {
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

.anomaly-overview {
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

.anomaly-trend {
  margin-bottom: 40px;
}

.chart-container {
  height: 300px;
}

.detail-content {
  padding: 20px;
}

.detail-content ul {
  margin: 0;
  padding-left: 20px;
}

.detail-content li {
  margin-bottom: 8px;
  color: #606266;
}
</style> 