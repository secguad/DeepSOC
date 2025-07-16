<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 顶部统计卡片 -->
      <el-col :span="6" v-for="(item, index) in statistics" :key="index">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" :style="{ backgroundColor: item.color }">
              <el-icon><component :is="item.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">{{ item.title }}</div>
              <div class="stat-value">{{ item.value }}</div>
              <div class="stat-trend" :class="item.trend >= 0 ? 'up' : 'down'">
                {{ Math.abs(item.trend) }}%
                <el-icon>
                  <component :is="item.trend >= 0 ? 'ArrowUp' : 'ArrowDown'" />
                </el-icon>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>安全事件趋势</span>
              <el-radio-group v-model="timeRange" size="small">
                <el-radio-button value="day">今日</el-radio-button>
                <el-radio-button value="week">本周</el-radio-button>
                <el-radio-button value="month">本月</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container" ref="trendChartRef"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>事件类型分布</span>
            </div>
          </template>
          <div class="chart-container" ref="pieChartRef"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最新告警列表 -->
    <el-card shadow="hover" class="alert-card">
      <template #header>
        <div class="card-header">
          <span>最新告警</span>
          <el-button type="primary" link>查看更多</el-button>
        </div>
      </template>
      <el-table :data="alerts" style="width: 100%">
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getAlertType(scope.row.type)">
              {{ scope.row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="level" label="等级" width="100">
          <template #default="scope">
            <el-tag :type="getLevelType(scope.row.level)">
              {{ scope.row.level }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="source" label="来源" width="150" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" link @click="handleAlertDetail(scope.row)">
              详情
            </el-button>
            <el-button type="success" link @click="handleAlertProcess(scope.row)">
              处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import {
  Warning,
  Monitor,
  Connection,
  DataLine
} from '@element-plus/icons-vue'

const timeRange = ref('day')
const trendChartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()

const statistics = ref([
  {
    title: '安全事件',
    value: '1,234',
    trend: 12.5,
    icon: 'Warning',
    color: '#f56c6c'
  },
  {
    title: '资产数量',
    value: '456',
    trend: -5.2,
    icon: 'Monitor',
    color: '#409eff'
  },
  {
    title: '漏洞数量',
    value: '89',
    trend: 8.3,
    icon: 'Connection',
    color: '#e6a23c'
  },
  {
    title: '安全评分',
    value: '85',
    trend: 2.1,
    icon: 'DataLine',
    color: '#67c23a'
  }
])

const alerts = ref([
  {
    time: '2024-02-20 10:00:00',
    type: '漏洞利用',
    level: '高危',
    source: '192.168.1.100',
    description: '检测到SQL注入攻击尝试',
    status: '未处理'
  },
  {
    time: '2024-02-20 10:05:00',
    type: '异常登录',
    level: '中危',
    source: '192.168.1.101',
    description: '检测到异常登录行为',
    status: '处理中'
  },
  {
    time: '2024-02-20 10:10:00',
    type: '配置变更',
    level: '低危',
    source: '192.168.1.102',
    description: '检测到系统配置变更',
    status: '已处理'
  }
])

const getAlertType = (type: string): string => {
  switch (type) {
    case '漏洞利用':
      return 'danger'
    case '异常登录':
      return 'warning'
    case '配置变更':
      return 'info'
    default:
      return 'info'
  }
}

const getLevelType = (level: string): string => {
  switch (level) {
    case '高危':
      return 'danger'
    case '中危':
      return 'warning'
    case '低危':
      return 'info'
    default:
      return 'info'
  }
}

const getStatusType = (status: string): string => {
  switch (status) {
    case '未处理':
      return 'danger'
    case '处理中':
      return 'warning'
    case '已处理':
      return 'success'
    default:
      return 'info'
  }
}

const handleAlertDetail = (row: any) => {
  console.log('查看告警详情:', row)
}

const handleAlertProcess = (row: any) => {
  console.log('处理告警:', row)
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
      data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '安全事件',
        type: 'line',
        smooth: true,
        data: [120, 132, 101, 134, 90, 230]
      }
    ]
  })

  // 初始化饼图
  const pieChart = echarts.init(pieChartRef.value!)
  pieChart.setOption({
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
          { value: 1048, name: '漏洞利用' },
          { value: 735, name: '异常登录' },
          { value: 580, name: '配置变更' },
          { value: 484, name: '其他' }
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
.dashboard {
  padding: 20px;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-icon :deep(.el-icon) {
  font-size: 24px;
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-trend {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-trend.up {
  color: #f56c6c;
}

.stat-trend.down {
  color: #67c23a;
}

.chart-row {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
}

.alert-card {
  margin-bottom: 20px;
}
</style> 