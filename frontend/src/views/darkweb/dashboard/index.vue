<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>今日告警数</span>
              <el-tag type="danger">{{ todayAlerts }}</el-tag>
            </div>
          </template>
          <div class="card-content">
            <el-icon class="icon"><Bell /></el-icon>
            <div class="trend">
              <span :class="{ 'up': alertTrend > 0, 'down': alertTrend < 0 }">
                {{ alertTrend > 0 ? '+' : '' }}{{ alertTrend }}%
              </span>
              较昨日
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>历史数据量</span>
              <el-tag type="success">{{ historyDataCount }}</el-tag>
            </div>
          </template>
          <div class="card-content">
            <el-icon class="icon"><DataLine /></el-icon>
            <div class="trend">
              <span :class="{ 'up': historyTrend > 0, 'down': historyTrend < 0 }">
                {{ historyTrend > 0 ? '+' : '' }}{{ historyTrend }}%
              </span>
              较上周
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>实时监控频道</span>
              <el-tag type="warning">{{ activeChannels }}</el-tag>
            </div>
          </template>
          <div class="card-content">
            <el-icon class="icon"><VideoPlay /></el-icon>
            <div class="trend">
              <span :class="{ 'up': channelTrend > 0, 'down': channelTrend < 0 }">
                {{ channelTrend > 0 ? '+' : '' }}{{ channelTrend }}%
              </span>
              较昨日
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>关键词数量</span>
              <el-tag type="info">{{ keywordCount }}</el-tag>
            </div>
          </template>
          <div class="card-content">
            <el-icon class="icon"><Edit /></el-icon>
            <div class="trend">
              <span :class="{ 'up': keywordTrend > 0, 'down': keywordTrend < 0 }">
                {{ keywordTrend > 0 ? '+' : '' }}{{ keywordTrend }}%
              </span>
              较上周
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>告警趋势</span>
              <el-radio-group v-model="alertTimeRange" size="small">
                <el-radio-button value="day">今日</el-radio-button>
                <el-radio-button value="week">本周</el-radio-button>
                <el-radio-button value="month">本月</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <!-- 这里将添加告警趋势图表 -->
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>告警类型分布</span>
            </div>
          </template>
          <div class="chart-container">
            <!-- 这里将添加告警类型分布图表 -->
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>实时告警</span>
            </div>
          </template>
          <el-table :data="realtimeAlerts" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180" />
            <el-table-column prop="type" label="类型" width="120" />
            <el-table-column prop="content" label="内容" />
            <el-table-column prop="level" label="级别" width="100">
              <template #default="scope">
                <el-tag :type="getAlertLevelType(scope.row.level)">
                  {{ scope.row.level }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>告警统计</span>
            </div>
          </template>
          <el-table :data="alertStats" style="width: 100%">
            <el-table-column prop="type" label="类型" width="120" />
            <el-table-column prop="count" label="数量" width="100" />
            <el-table-column prop="percentage" label="占比">
              <template #default="scope">
                <el-progress :percentage="scope.row.percentage" />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Bell, DataLine, VideoPlay, Edit } from '@element-plus/icons-vue'

// 数据统计
const todayAlerts = ref(12)
const alertTrend = ref(15)
const historyDataCount = ref(1234)
const historyTrend = ref(-5)
const activeChannels = ref(8)
const channelTrend = ref(0)
const keywordCount = ref(50)
const keywordTrend = ref(10)

// 告警时间范围
const alertTimeRange = ref('day')

// 实时告警数据
const realtimeAlerts = ref([
  {
    time: '2024-03-29 10:30:00',
    type: '账号泄露',
    content: '发现公司邮箱账号在暗网论坛泄露',
    level: '高'
  },
  {
    time: '2024-03-29 10:25:00',
    type: '文档泄露',
    content: '发现内部文档在暗网交易平台出现',
    level: '中'
  },
  {
    time: '2024-03-29 10:20:00',
    type: '代码泄露',
    content: '发现源代码在GitHub泄露',
    level: '高'
  }
])

// 告警统计
const alertStats = ref([
  {
    type: '账号泄露',
    count: 5,
    percentage: 40
  },
  {
    type: '文档泄露',
    count: 3,
    percentage: 25
  },
  {
    type: '代码泄露',
    count: 2,
    percentage: 15
  },
  {
    type: '其他',
    count: 2,
    percentage: 20
  }
])

// 获取告警级别对应的标签类型
const getAlertLevelType = (level: string) => {
  switch (level) {
    case '高':
      return 'danger'
    case '中':
      return 'warning'
    case '低':
      return 'info'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.data-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.icon {
  font-size: 48px;
  color: #409EFF;
}

.trend {
  font-size: 14px;
  color: #909399;
}

.trend .up {
  color: #67C23A;
}

.trend .down {
  color: #F56C6C;
}

.chart-row {
  margin-top: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-container {
  height: 300px;
}
</style> 