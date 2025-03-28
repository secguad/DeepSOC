<template>
  <div class="risk">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>风险评估</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleScan">开始评估</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 风险概览 -->
      <div class="risk-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">总体风险等级</div>
                <div class="overview-value">中风险</div>
                <div class="overview-trend">
                  较上期
                  <span class="down">
                    10%
                    <el-icon><ArrowDown /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">高风险资产</div>
                <div class="overview-value">5</div>
                <div class="overview-trend">
                  较上期
                  <span class="down">
                    2
                    <el-icon><ArrowDown /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">待处理风险</div>
                <div class="overview-value">12</div>
                <div class="overview-trend">
                  较上期
                  <span class="down">
                    3
                    <el-icon><ArrowDown /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 风险趋势 -->
      <div class="risk-trend">
        <div class="section-title">风险趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>风险评分趋势</span>
                  <el-select v-model="timeRange" size="small">
                    <el-option label="近7天" value="7" />
                    <el-option label="近30天" value="30" />
                    <el-option label="近90天" value="90" />
                  </el-select>
                </div>
              </template>
              <div class="chart-container" ref="riskTrendChartRef"></div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>风险类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="riskTypeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 风险列表 -->
      <div class="risk-list">
        <div class="section-title">风险列表</div>
        <el-table :data="riskList" style="width: 100%">
          <el-table-column prop="id" label="风险ID" width="120" />
          <el-table-column prop="name" label="风险名称" />
          <el-table-column prop="type" label="风险类型" width="120">
            <template #default="scope">
              <el-tag :type="getRiskTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="level" label="风险等级" width="100">
            <template #default="scope">
              <el-tag :type="getRiskLevelTag(scope.row.level)">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="asset" label="影响资产" width="150" />
          <el-table-column prop="discoveryTime" label="发现时间" width="180" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getRiskStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleMitigate(scope.row)">
                缓解
              </el-button>
              <el-button type="warning" link @click="handleVerify(scope.row)">
                验证
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 风险详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="风险详情"
      width="800px"
    >
      <div v-if="currentRisk" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="风险ID">{{ currentRisk.id }}</el-descriptions-item>
          <el-descriptions-item label="风险名称">{{ currentRisk.name }}</el-descriptions-item>
          <el-descriptions-item label="风险类型">
            <el-tag :type="getRiskTypeTag(currentRisk.type)">
              {{ currentRisk.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag :type="getRiskLevelTag(currentRisk.level)">
              {{ currentRisk.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="影响资产">{{ currentRisk.asset }}</el-descriptions-item>
          <el-descriptions-item label="发现时间">{{ currentRisk.discoveryTime }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getRiskStatusTag(currentRisk.status)">
              {{ currentRisk.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ currentRisk.description }}</el-descriptions-item>
          <el-descriptions-item label="影响" :span="2">{{ currentRisk.impact }}</el-descriptions-item>
          <el-descriptions-item label="建议措施" :span="2">{{ currentRisk.suggestion }}</el-descriptions-item>
          <el-descriptions-item label="处理记录" :span="2">
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in currentRisk.activities"
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
import { ArrowDown } from '@element-plus/icons-vue'

// 定义图表引用
const riskTrendChartRef = ref<HTMLElement | null>(null)
const riskTypeChartRef = ref<HTMLElement | null>(null)

const timeRange = ref('7')

// 风险列表数据
const riskList = ref([
  {
    id: 'RISK-2024-001',
    name: '未授权访问风险',
    type: '访问控制',
    level: '高危',
    asset: 'Web服务器-01',
    discoveryTime: '2024-02-20 10:00:00',
    status: '待处理',
    description: '检测到Web服务器存在未授权访问漏洞，可能导致敏感信息泄露。',
    impact: '可能导致敏感信息泄露，系统被未授权访问。',
    suggestion: '1. 实施严格的访问控制策略\n2. 配置IP白名单\n3. 启用双因素认证',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'warning',
        content: '发现未授权访问风险'
      }
    ]
  },
  {
    id: 'RISK-2024-002',
    name: '弱密码风险',
    type: '认证安全',
    level: '中危',
    asset: '数据库服务器-01',
    discoveryTime: '2024-02-20 09:30:00',
    status: '处理中',
    description: '检测到数据库服务器存在弱密码账户。',
    impact: '可能导致账户被暴力破解，数据泄露。',
    suggestion: '1. 强制修改弱密码\n2. 实施密码复杂度要求\n3. 启用登录失败限制',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'warning',
        content: '发现弱密码风险'
      },
      {
        time: '2024-02-20 09:45:00',
        type: 'primary',
        content: '开始处理风险'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentRisk = ref<any>(null)

const getRiskTypeTag = (type: string): string => {
  switch (type) {
    case '访问控制':
      return 'danger'
    case '认证安全':
      return 'warning'
    case '数据安全':
      return 'info'
    default:
      return ''
  }
}

const getRiskLevelTag = (level: string): string => {
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

const getRiskStatusTag = (status: string): string => {
  switch (status) {
    case '待处理':
      return 'danger'
    case '处理中':
      return 'warning'
    case '已处理':
      return 'success'
    default:
      return ''
  }
}

const handleScan = () => {
  ElMessage.success('开始风险评估...')
}

const handleExport = () => {
  ElMessage.success('导出风险评估报告...')
}

const handleDetail = (row: any) => {
  currentRisk.value = row
  detailVisible.value = true
}

const handleMitigate = (row: any) => {
  ElMessage.success('开始风险缓解...')
}

const handleVerify = (row: any) => {
  ElMessage.success('开始风险验证...')
}

onMounted(() => {
  // 初始化风险趋势图
  const riskTrendChart = echarts.init(riskTrendChartRef.value!)
  riskTrendChart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['2-14', '2-15', '2-16', '2-17', '2-18', '2-19', '2-20']
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100
    },
    series: [
      {
        name: '风险评分',
        type: 'line',
        data: [85, 82, 80, 78, 75, 73, 70],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })

  // 初始化风险类型分布图
  const riskTypeChart = echarts.init(riskTypeChartRef.value!)
  riskTypeChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '风险类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '访问控制' },
          { value: 30, name: '认证安全' },
          { value: 20, name: '数据安全' },
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
.risk {
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

.risk-overview {
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

.risk-trend {
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