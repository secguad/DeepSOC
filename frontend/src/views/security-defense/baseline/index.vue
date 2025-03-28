<template>
  <div class="baseline">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>基线核查</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleScan">开始核查</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 基线概览 -->
      <div class="baseline-overview">
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

      <!-- 基线趋势 -->
      <div class="baseline-trend">
        <div class="section-title">基线趋势</div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>合规率趋势</span>
                  <el-select v-model="timeRange" size="small">
                    <el-option label="近7天" value="7" />
                    <el-option label="近30天" value="30" />
                    <el-option label="近90天" value="90" />
                  </el-select>
                </div>
              </template>
              <div class="chart-container" ref="complianceChartRef"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>基线项分布</span>
                </div>
              </template>
              <div class="chart-container" ref="baselineChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 基线列表 -->
      <div class="baseline-list">
        <div class="section-title">基线列表</div>
        <el-table :data="baselineList" style="width: 100%">
          <el-table-column prop="id" label="基线ID" width="120" />
          <el-table-column prop="name" label="基线名称" width="200" />
          <el-table-column prop="type" label="基线类型" width="120">
            <template #default="scope">
              <el-tag :type="getBaselineTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="compliance" label="合规率" width="120">
            <template #default="scope">
              <el-progress 
                :percentage="scope.row.compliance" 
                :status="getComplianceStatus(scope.row.compliance)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="total" label="检查项" width="100" />
          <el-table-column prop="passed" label="通过项" width="100" />
          <el-table-column prop="failed" label="未通过项" width="100" />
          <el-table-column prop="lastCheckTime" label="最后检查时间" width="180" />
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleFix(scope.row)">
                修复
              </el-button>
              <el-button type="warning" link @click="handleVerify(scope.row)">
                验证
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 基线详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="基线详情"
      width="800px"
    >
      <div v-if="currentBaseline" class="baseline-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="基线ID">{{ currentBaseline.id }}</el-descriptions-item>
          <el-descriptions-item label="基线名称">{{ currentBaseline.name }}</el-descriptions-item>
          <el-descriptions-item label="基线类型">
            <el-tag :type="getBaselineTypeTag(currentBaseline.type)">
              {{ currentBaseline.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="合规率">
            <el-progress 
              :percentage="currentBaseline.compliance" 
              :status="getComplianceStatus(currentBaseline.compliance)"
            />
          </el-descriptions-item>
          <el-descriptions-item label="检查项总数">{{ currentBaseline.total }}</el-descriptions-item>
          <el-descriptions-item label="通过项数">{{ currentBaseline.passed }}</el-descriptions-item>
          <el-descriptions-item label="未通过项数">{{ currentBaseline.failed }}</el-descriptions-item>
          <el-descriptions-item label="最后检查时间">{{ currentBaseline.lastCheckTime }}</el-descriptions-item>
          <el-descriptions-item label="基线描述" :span="2">{{ currentBaseline.description }}</el-descriptions-item>
          <el-descriptions-item label="检查结果" :span="2">
            <el-table :data="currentBaseline.items" style="width: 100%">
              <el-table-column prop="name" label="检查项" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === '通过' ? 'success' : 'danger'">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="result" label="检查结果" />
              <el-table-column prop="suggestion" label="修复建议" />
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
const complianceChartRef = ref<HTMLElement | null>(null)
const baselineChartRef = ref<HTMLElement | null>(null)

// 定义基线类型接口
interface BaselineItem {
  name: string
  status: string
  result: string
  suggestion: string
}

interface Baseline {
  id: string
  name: string
  type: string
  compliance: number
  total: number
  passed: number
  failed: number
  lastCheckTime: string
  description: string
  items: BaselineItem[]
}

const overview = ref([
  {
    title: '基线总数',
    value: '12',
    trend: 0
  },
  {
    title: '合规基线',
    value: '8',
    trend: 10
  },
  {
    title: '待修复',
    value: '4',
    trend: -20
  },
  {
    title: '平均合规率',
    value: '85%',
    trend: 5
  }
])

const timeRange = ref('7')

const baselineList = ref<Baseline[]>([
  {
    id: 'BL-2024-001',
    name: 'Linux系统安全基线',
    type: '操作系统',
    compliance: 92,
    total: 50,
    passed: 46,
    failed: 4,
    lastCheckTime: '2024-02-20 10:00:00',
    description: 'Linux系统安全配置基线检查，包括密码策略、权限管理、服务配置等。',
    items: [
      {
        name: '密码复杂度要求',
        status: '通过',
        result: '符合要求',
        suggestion: '-'
      },
      {
        name: 'SSH配置检查',
        status: '未通过',
        result: '允许root远程登录',
        suggestion: '修改SSH配置，禁止root远程登录'
      }
    ]
  },
  {
    id: 'BL-2024-002',
    name: 'Web服务器安全基线',
    type: '应用服务',
    compliance: 78,
    total: 40,
    passed: 31,
    failed: 9,
    lastCheckTime: '2024-02-20 09:30:00',
    description: 'Web服务器安全配置基线检查，包括SSL配置、访问控制、日志配置等。',
    items: [
      {
        name: 'SSL配置检查',
        status: '通过',
        result: '符合要求',
        suggestion: '-'
      },
      {
        name: '目录访问控制',
        status: '未通过',
        result: '存在目录遍历风险',
        suggestion: '配置目录访问控制，禁止目录遍历'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentBaseline = ref<Baseline | null>(null)

const getBaselineTypeTag = (type: string): string => {
  switch (type) {
    case '操作系统':
      return 'primary'
    case '应用服务':
      return 'success'
    case '数据库':
      return 'warning'
    case '网络设备':
      return 'info'
    default:
      return ''
  }
}

const getComplianceStatus = (compliance: number): string => {
  if (compliance >= 90) return 'success'
  if (compliance >= 70) return 'warning'
  return 'exception'
}

const handleScan = () => {
  ElMessage.success('开始基线核查...')
}

const handleExport = () => {
  ElMessage.success('导出报告...')
}

const handleDetail = (row: Baseline) => {
  currentBaseline.value = row
  detailVisible.value = true
}

const handleFix = (row: Baseline) => {
  ElMessage.success(`开始修复基线：${row.name}`)
}

const handleVerify = (row: Baseline) => {
  ElMessage.success(`开始验证基线：${row.name}`)
}

onMounted(() => {
  // 初始化合规率趋势图
  const complianceChart = echarts.init(complianceChartRef.value!)
  complianceChart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['2-14', '2-15', '2-16', '2-17', '2-18', '2-19', '2-20']
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: '合规率',
        type: 'line',
        data: [80, 82, 83, 84, 85, 85, 85],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })

  // 初始化基线项分布图
  const baselineChart = echarts.init(baselineChartRef.value!)
  baselineChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '基线类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 5, name: '操作系统' },
          { value: 4, name: '应用服务' },
          { value: 2, name: '数据库' },
          { value: 1, name: '网络设备' }
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
.baseline {
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

.baseline-overview {
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

.baseline-trend {
  margin-bottom: 40px;
}

.chart-container {
  height: 300px;
}

.baseline-detail {
  padding: 20px;
}
</style> 