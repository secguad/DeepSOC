<template>
  <div class="score">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="score-card" shadow="hover">
          <div class="total-score">
            <div class="score-circle">
              <el-progress 
                type="circle" 
                :percentage="totalScore" 
                :color="getScoreColor"
                :format="(percentage) => percentage + '分'"
              />
            </div>
            <div class="score-info">
              <div class="score-title">总体安全评分</div>
              <div class="score-trend">
                较上期
                <span :class="scoreTrend >= 0 ? 'up' : 'down'">
                  {{ scoreTrend >= 0 ? '+' : '' }}{{ scoreTrend }}
                  <el-icon>
                    <CaretTop v-if="scoreTrend >= 0"/>
                    <CaretBottom v-else/>
                  </el-icon>
                </span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card class="trend-card" shadow="hover">
          <div ref="scoreChartRef" class="score-chart"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 分项评分 -->
    <el-card class="detail-card">
      <template #header>
        <div class="card-header">
          <span>分项评分</span>
          <el-radio-group v-model="detailType" size="small">
            <el-radio-button label="category">按类别</el-radio-button>
            <el-radio-button label="department">按部门</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <el-table :data="scoreDetails" style="width: 100%">
        <el-table-column prop="name" label="评分项" width="180"/>
        <el-table-column prop="score" label="得分" width="120">
          <template #default="scope">
            <span :style="{ color: getTextColor(scope.row.score) }">
              {{ scope.row.score }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="weight" label="权重" width="120"/>
        <el-table-column prop="trend" label="趋势" width="120">
          <template #default="scope">
            <span :class="scope.row.trend >= 0 ? 'up' : 'down'">
              {{ scope.row.trend >= 0 ? '+' : '' }}{{ scope.row.trend }}
              <el-icon>
                <CaretTop v-if="scope.row.trend >= 0"/>
                <CaretBottom v-else/>
              </el-icon>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="说明"/>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { CaretTop, CaretBottom } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 基础数据
const totalScore = ref(85)
const scoreTrend = ref(5)
const detailType = ref('category')

// 图表引用
const scoreChartRef = ref<HTMLElement>()
let scoreChart: echarts.ECharts | null = null

// 分项评分数据
const scoreDetails = ref([
  {
    name: '漏洞管理',
    score: 88,
    weight: '20%',
    trend: 3,
    description: '包括漏洞扫描、修复和验证等环节'
  },
  {
    name: '安全配置',
    score: 92,
    weight: '15%',
    trend: -2,
    description: '系统和应用的安全配置达标情况'
  },
  {
    name: '威胁检测',
    score: 78,
    weight: '25%',
    trend: 8,
    description: '安全设备的检测和响应能力'
  }
])

// 评分颜色计算
const getScoreColor = (percentage: number) => {
  if (percentage < 60) return '#F56C6C'
  if (percentage < 80) return '#E6A23C'
  return '#67C23A'
}

// 文字颜色计算
const getTextColor = (score: number) => {
  if (score < 60) return '#F56C6C'
  if (score < 80) return '#E6A23C'
  return '#67C23A'
}

// 初始化图表
const initChart = () => {
  if (scoreChartRef.value) {
    scoreChart = echarts.init(scoreChartRef.value)
    const option = {
      title: {
        text: '评分趋势'
      },
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
          name: '总分',
          type: 'line',
          data: [75, 78, 82, 80, 85, 85],
          smooth: true,
          markPoint: {
            data: [
              { type: 'max', name: '最高分' },
              { type: 'min', name: '最低分' }
            ]
          }
        }
      ]
    }
    scoreChart.setOption(option)
  }
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', () => {
    scoreChart?.resize()
  })
})

onUnmounted(() => {
  scoreChart?.dispose()
  window.removeEventListener('resize', () => {
    scoreChart?.resize()
  })
})
</script>

<style scoped>
.score {
  padding: 20px;
}

.score-card {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.total-score {
  display: flex;
  align-items: center;
  gap: 20px;
}

.score-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.score-title {
  font-size: 16px;
  font-weight: bold;
}

.score-trend {
  font-size: 14px;
  color: #909399;
}

.trend-card {
  height: 200px;
}

.score-chart {
  height: 180px;
}

.detail-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.up {
  color: #67C23A;
}

.down {
  color: #F56C6C;
}
</style> 