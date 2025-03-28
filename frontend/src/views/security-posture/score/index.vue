<template>
  <div class="score">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>量化评分</span>
          <div class="header-actions">
            <el-button type="primary">导出报告</el-button>
            <el-button type="success" style="margin-left: 16px">重新评分</el-button>
          </div>
        </div>
      </template>

      <!-- 总体评分 -->
      <div class="overall-score">
        <div class="score-circle">
          <el-progress
            type="circle"
            :percentage="overallScore"
            :color="getScoreColor"
            :stroke-width="10"
            :width="200"
          >
            <template #default="{ percentage }">
              <div class="score-content">
                <div class="score-value">{{ percentage }}</div>
                <div class="score-label">总体评分</div>
              </div>
            </template>
          </el-progress>
        </div>
        <div class="score-details">
          <div class="detail-item">
            <span class="label">上次评分</span>
            <span class="value">{{ lastScore }}</span>
          </div>
          <div class="detail-item">
            <span class="label">评分时间</span>
            <span class="value">{{ scoreTime }}</span>
          </div>
          <div class="detail-item">
            <span class="label">评分周期</span>
            <span class="value">{{ scorePeriod }}</span>
          </div>
        </div>
      </div>

      <!-- 评分维度 -->
      <div class="score-dimensions">
        <div class="section-title">评分维度</div>
        <el-row :gutter="20">
          <el-col :span="8" v-for="(dimension, index) in dimensions" :key="index">
            <el-card shadow="hover" class="dimension-card">
              <div class="dimension-header">
                <span class="dimension-name">{{ dimension.name }}</span>
                <el-tag :type="getDimensionType(dimension.score)">{{ dimension.score }}</el-tag>
              </div>
              <el-progress
                :percentage="dimension.score"
                :color="getDimensionColor(dimension.score)"
                :show-text="false"
                :stroke-width="8"
                class="dimension-progress"
              />
              <div class="dimension-details">
                <div class="detail-row">
                  <span>权重</span>
                  <span>{{ dimension.weight }}%</span>
                </div>
                <div class="detail-row">
                  <span>得分</span>
                  <span>{{ dimension.score }}</span>
                </div>
                <div class="detail-row">
                  <span>贡献值</span>
                  <span>{{ dimension.contribution }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 评分趋势 -->
      <div class="score-trend">
        <div class="section-title">评分趋势</div>
        <div class="chart-container" ref="trendChartRef"></div>
      </div>

      <!-- 扣分项 -->
      <div class="deduction-items">
        <div class="section-title">扣分项</div>
        <el-table :data="deductions" style="width: 100%">
          <el-table-column prop="category" label="类别" width="120" />
          <el-table-column prop="item" label="扣分项" />
          <el-table-column prop="score" label="扣分" width="100">
            <template #default="scope">
              <span class="deduction-score">-{{ scope.row.score }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="原因" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getDeductionStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDeductionDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleDeductionFix(scope.row)">
                整改
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import * as echarts from 'echarts'

const overallScore = ref(85)
const lastScore = ref(82)
const scoreTime = ref('2024-02-20 10:00:00')
const scorePeriod = ref('2024-02-01 至 2024-02-20')

const dimensions = ref([
  {
    name: '资产安全',
    score: 90,
    weight: 30,
    contribution: 27
  },
  {
    name: '漏洞管理',
    score: 85,
    weight: 25,
    contribution: 21.25
  },
  {
    name: '安全事件',
    score: 80,
    weight: 20,
    contribution: 16
  },
  {
    name: '合规管理',
    score: 88,
    weight: 15,
    contribution: 13.2
  },
  {
    name: '安全运营',
    score: 92,
    weight: 10,
    contribution: 9.2
  }
])

const deductions = ref([
  {
    category: '漏洞管理',
    item: '高危漏洞未及时修复',
    score: 5,
    reason: '发现3个高危漏洞超过修复期限',
    status: '待整改'
  },
  {
    category: '安全事件',
    item: '安全事件响应超时',
    score: 3,
    reason: '2起安全事件响应时间超过SLA',
    status: '整改中'
  },
  {
    category: '合规管理',
    item: '安全配置不合规',
    score: 2,
    reason: '5台服务器安全配置不符合基线要求',
    status: '已整改'
  }
])

const getScoreColor = computed(() => {
  if (overallScore.value >= 90) return '#67c23a'
  if (overallScore.value >= 80) return '#409eff'
  if (overallScore.value >= 70) return '#e6a23c'
  return '#f56c6c'
})

const getDimensionType = (score: number): string => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'primary'
  if (score >= 70) return 'warning'
  return 'danger'
}

const getDimensionColor = (score: number): string => {
  if (score >= 90) return '#67c23a'
  if (score >= 80) return '#409eff'
  if (score >= 70) return '#e6a23c'
  return '#f56c6c'
}

const getDeductionStatusType = (status: string): string => {
  switch (status) {
    case '待整改':
      return 'danger'
    case '整改中':
      return 'warning'
    case '已整改':
      return 'success'
    default:
      return 'info'
  }
}

const handleDeductionDetail = (row: any) => {
  console.log('查看扣分详情:', row)
}

const handleDeductionFix = (row: any) => {
  console.log('整改扣分项:', row)
}

onMounted(() => {
  const trendChart = echarts.init(trendChartRef.value!)
  trendChart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月']
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100
    },
    series: [
      {
        name: '总体评分',
        type: 'line',
        smooth: true,
        data: [78, 82, 85, 83, 85, 85],
        itemStyle: {
          color: '#409eff'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgba(64,158,255,0.3)'
            },
            {
              offset: 1,
              color: 'rgba(64,158,255,0.1)'
            }
          ])
        }
      }
    ]
  })
})
</script>

<style scoped>
.score {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.overall-score {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 40px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.score-circle {
  margin-right: 40px;
}

.score-content {
  text-align: center;
}

.score-value {
  font-size: 36px;
  font-weight: bold;
  color: #303133;
}

.score-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}

.score-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item .label {
  font-size: 14px;
  color: #909399;
}

.detail-item .value {
  font-size: 16px;
  color: #303133;
  font-weight: bold;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 20px;
}

.dimension-card {
  margin-bottom: 20px;
}

.dimension-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.dimension-name {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.dimension-progress {
  margin-bottom: 16px;
}

.dimension-details {
  display: flex;
  justify-content: space-between;
}

.detail-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.detail-row span:first-child {
  font-size: 12px;
  color: #909399;
}

.detail-row span:last-child {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.chart-container {
  height: 300px;
  margin-bottom: 40px;
}

.deduction-score {
  color: #f56c6c;
  font-weight: bold;
}
</style> 