<template>
  <div class="analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>智能分析</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAnalyze">开始分析</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 分析概览 -->
      <div class="analysis-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">今日分析</div>
                <div class="overview-value">28</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    5
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">发现威胁</div>
                <div class="overview-value">12</div>
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
                <div class="overview-title">分析规则</div>
                <div class="overview-value">18</div>
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

      <!-- 分析趋势 -->
      <div class="analysis-trend">
        <div class="section-title">分析趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>分析数据趋势</span>
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
                  <span>分析类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="typeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 分析列表 -->
      <div class="analysis-list">
        <div class="section-title">分析列表</div>
        <el-table :data="analysisList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="name" label="分析名称" />
          <el-table-column prop="type" label="分析类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="time" label="分析时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleVisualize(scope.row)">
                可视化
              </el-button>
              <el-button type="warning" link @click="handleExport(scope.row)">
                导出
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="分析详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="分析名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="分析类型">
            <el-tag :type="getTypeTag(currentItem.type)">
              {{ currentItem.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTag(currentItem.status)">
              {{ currentItem.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="分析时间">{{ currentItem.time }}</el-descriptions-item>
          <el-descriptions-item label="分析规则">{{ currentItem.rule }}</el-descriptions-item>
          <el-descriptions-item label="分析结果" :span="2">{{ currentItem.result }}</el-descriptions-item>
          <el-descriptions-item label="建议措施" :span="2">{{ currentItem.suggestion }}</el-descriptions-item>
          <el-descriptions-item label="操作记录" :span="2">
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

// 分析列表数据
const analysisList = ref([
  {
    id: 'ANALYSIS-2024-001',
    name: '安全事件分析',
    type: '威胁分析',
    status: '已完成',
    time: '2024-02-20 10:00:00',
    rule: '基于机器学习的异常检测',
    result: '发现3个高风险威胁，5个中风险威胁',
    suggestion: '建议立即处理高风险威胁，并加强系统监控',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'primary',
        content: '开始分析'
      },
      {
        time: '2024-02-20 10:05:00',
        type: 'success',
        content: '分析完成'
      }
    ]
  },
  {
    id: 'ANALYSIS-2024-002',
    name: '用户行为分析',
    type: '行为分析',
    status: '分析中',
    time: '2024-02-20 09:30:00',
    rule: '基于规则的异常行为检测',
    result: '正在分析用户行为数据...',
    suggestion: '等待分析完成',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'primary',
        content: '开始分析'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '威胁分析':
      return 'danger'
    case '行为分析':
      return 'warning'
    case '漏洞分析':
      return 'info'
    default:
      return ''
  }
}

const getStatusTag = (status: string): string => {
  switch (status) {
    case '已完成':
      return 'success'
    case '分析中':
      return 'primary'
    case '失败':
      return 'danger'
    default:
      return ''
  }
}

const handleAnalyze = (row: any) => {
  ElMessage.success(`开始分析: ${row.name}`)
}

const handleExport = (row: any) => {
  ElMessage.success(`导出分析报告: ${row.name}`)
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleVisualize = (row: any) => {
  ElMessage.success(`开始可视化: ${row.name}`)
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
        name: '分析数量',
        type: 'line',
        data: [25, 30, 28, 35, 32, 38, 28],
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
        name: '分析类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '威胁分析' },
          { value: 30, name: '行为分析' },
          { value: 20, name: '漏洞分析' },
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
.analysis {
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

.analysis-overview {
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

.analysis-trend {
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