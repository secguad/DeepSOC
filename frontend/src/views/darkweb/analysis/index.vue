<template>
  <div class="darkweb-analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据分析</span>
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
                <div class="overview-title">数据总量</div>
                <div class="overview-value">1,234</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    123
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">有效数据</div>
                <div class="overview-value">986</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    89
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">数据源数量</div>
                <div class="overview-value">45</div>
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
                  <span>数据采集趋势</span>
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
                  <span>数据来源分布</span>
                </div>
              </template>
              <div class="chart-container" ref="sourceChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 分析列表 -->
      <div class="analysis-list">
        <div class="section-title">分析列表</div>
        <el-table :data="analysisList" style="width: 100%">
          <el-table-column prop="id" label="分析ID" width="120" />
          <el-table-column prop="name" label="分析名称" />
          <el-table-column prop="type" label="分析类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="dataSource" label="数据来源" width="150" />
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
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
          <el-descriptions-item label="分析ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="分析名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="分析类型">
            <el-tag :type="getTypeTag(currentItem.type)">
              {{ currentItem.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="数据来源">{{ currentItem.dataSource }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentItem.createTime }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTag(currentItem.status)">
              {{ currentItem.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="分析描述" :span="2">{{ currentItem.description }}</el-descriptions-item>
          <el-descriptions-item label="分析结果" :span="2">{{ currentItem.result }}</el-descriptions-item>
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
const sourceChartRef = ref<HTMLElement | null>(null)

const timeRange = ref('7')

// 分析列表数据
const analysisList = ref([
  {
    id: 'ANALYSIS-2024-001',
    name: '敏感信息泄露分析',
    type: '信息分析',
    dataSource: '暗网论坛',
    createTime: '2024-02-20 10:00:00',
    status: '已完成',
    description: '分析近期敏感信息泄露情况，包括泄露渠道、影响范围等。',
    result: '1. 发现3个主要泄露渠道\n2. 影响范围涉及5个部门\n3. 建议加强数据安全防护',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'primary',
        content: '开始数据分析'
      },
      {
        time: '2024-02-20 10:30:00',
        type: 'success',
        content: '分析完成'
      }
    ]
  },
  {
    id: 'ANALYSIS-2024-002',
    name: '威胁情报分析',
    type: '威胁分析',
    dataSource: '黑客论坛',
    createTime: '2024-02-20 09:30:00',
    status: '分析中',
    description: '分析近期针对公司的威胁情报，评估潜在风险。',
    result: '1. 发现2个潜在威胁\n2. 风险等级评估为中\n3. 建议加强系统防护',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'primary',
        content: '开始威胁分析'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '信息分析':
      return 'danger'
    case '威胁分析':
      return 'warning'
    case '趋势分析':
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
      return 'warning'
    case '已失败':
      return 'danger'
    default:
      return ''
  }
}

const handleAnalyze = () => {
  ElMessage.success('开始数据分析...')
}

const handleExport = (row?: any) => {
  if (row) {
    ElMessage.success(`导出分析报告: ${row.name}`)
  } else {
    ElMessage.success('导出所有分析报告...')
  }
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleVisualize = (row: any) => {
  ElMessage.success(`开始可视化分析: ${row.name}`)
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
        name: '数据量',
        type: 'line',
        data: [150, 230, 224, 218, 135, 147, 260],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })

  // 初始化来源分布图
  const sourceChart = echarts.init(sourceChartRef.value!)
  sourceChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '数据来源',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '暗网论坛' },
          { value: 30, name: '黑客论坛' },
          { value: 20, name: '数据交易' },
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
.darkweb-analysis {
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