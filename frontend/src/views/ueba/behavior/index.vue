<template>
  <div class="ueba-behavior">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户行为分析</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAnalyze">开始分析</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 行为概览 -->
      <div class="behavior-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">异常行为</div>
                <div class="overview-value">12</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    3
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">风险用户</div>
                <div class="overview-value">8</div>
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
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">行为规则</div>
                <div class="overview-value">15</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    1
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 行为趋势 -->
      <div class="behavior-trend">
        <div class="section-title">行为趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>异常行为趋势</span>
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
                  <span>行为类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="typeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 行为列表 -->
      <div class="behavior-list">
        <div class="section-title">行为列表</div>
        <el-table :data="behaviorList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="user" label="用户" />
          <el-table-column prop="type" label="行为类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="risk" label="风险等级" width="100">
            <template #default="scope">
              <el-tag :type="getRiskTag(scope.row.risk)">
                {{ scope.row.risk }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="time" label="发生时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="warning" link @click="handleInvestigate(scope.row)">
                调查
              </el-button>
              <el-button type="danger" link @click="handleBlock(scope.row)">
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
      title="行为详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="用户">{{ currentItem.user }}</el-descriptions-item>
          <el-descriptions-item label="行为类型">
            <el-tag :type="getTypeTag(currentItem.type)">
              {{ currentItem.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag :type="getRiskTag(currentItem.risk)">
              {{ currentItem.risk }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="发生时间">{{ currentItem.time }}</el-descriptions-item>
          <el-descriptions-item label="IP地址">{{ currentItem.ip }}</el-descriptions-item>
          <el-descriptions-item label="行为描述" :span="2">{{ currentItem.description }}</el-descriptions-item>
          <el-descriptions-item label="影响范围" :span="2">{{ currentItem.impact }}</el-descriptions-item>
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
import { ArrowUp } from '@element-plus/icons-vue'

// 定义图表引用
const trendChartRef = ref<HTMLElement | null>(null)
const typeChartRef = ref<HTMLElement | null>(null)

const timeRange = ref('7')

// 行为列表数据
const behaviorList = ref([
  {
    id: 'BEHAVIOR-2024-001',
    user: 'admin',
    type: '异常登录',
    risk: '高风险',
    time: '2024-02-20 10:00:00',
    ip: '192.168.1.100',
    description: '在非工作时间段尝试登录系统',
    impact: '可能涉及系统安全',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'danger',
        content: '检测到异常登录行为'
      }
    ]
  },
  {
    id: 'BEHAVIOR-2024-002',
    user: 'user1',
    type: '数据导出',
    risk: '中风险',
    time: '2024-02-20 09:30:00',
    ip: '192.168.1.101',
    description: '短时间内大量导出敏感数据',
    impact: '可能涉及数据泄露',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'warning',
        content: '检测到异常数据导出行为'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '异常登录':
      return 'danger'
    case '数据导出':
      return 'warning'
    case '权限变更':
      return 'info'
    default:
      return ''
  }
}

const getRiskTag = (risk: string): string => {
  switch (risk) {
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

const handleAnalyze = () => {
  ElMessage.success('开始分析用户行为...')
}

const handleExport = () => {
  ElMessage.success('导出分析报告...')
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleInvestigate = (row: any) => {
  ElMessage.success(`开始调查行为: ${row.id}`)
}

const handleBlock = (row: any) => {
  ElMessage.success(`已阻断用户: ${row.user}`)
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
        name: '异常行为数',
        type: 'line',
        data: [5, 8, 3, 9, 6, 7, 12],
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
        name: '行为类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '异常登录' },
          { value: 30, name: '数据导出' },
          { value: 20, name: '权限变更' },
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
.ueba-behavior {
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

.behavior-overview {
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

.behavior-trend {
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