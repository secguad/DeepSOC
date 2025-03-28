<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 安全评分 -->
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="score-card">
            <div class="score-title">安全评分</div>
            <div class="score-value">85</div>
            <div class="score-trend">
              较上期
              <span class="up">
                5%
                <el-icon><ArrowUp /></el-icon>
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 告警统计 -->
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="alert-card">
            <div class="alert-title">今日告警</div>
            <div class="alert-value">12</div>
            <div class="alert-trend">
              较上期
              <span class="down">
                20%
                <el-icon><ArrowDown /></el-icon>
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 漏洞统计 -->
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="vuln-card">
            <div class="vuln-title">待处理漏洞</div>
            <div class="vuln-value">8</div>
            <div class="vuln-trend">
              较上期
              <span class="down">
                15%
                <el-icon><ArrowDown /></el-icon>
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 资产统计 -->
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="asset-card">
            <div class="asset-title">资产总数</div>
            <div class="asset-value">156</div>
            <div class="asset-trend">
              较上期
              <span class="up">
                3%
                <el-icon><ArrowUp /></el-icon>
              </span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 告警趋势 -->
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>告警趋势</span>
              <el-select v-model="timeRange" size="small">
                <el-option label="近7天" value="7" />
                <el-option label="近30天" value="30" />
                <el-option label="近90天" value="90" />
              </el-select>
            </div>
          </template>
          <div class="chart-container" ref="alertTrendChartRef"></div>
        </el-card>
      </el-col>
      <!-- 告警类型分布 -->
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>告警类型分布</span>
            </div>
          </template>
          <div class="chart-container" ref="alertTypeChartRef"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 最新告警 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>最新告警</span>
            </div>
          </template>
          <el-table :data="latestAlerts" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180" />
            <el-table-column prop="type" label="类型" width="120">
              <template #default="scope">
                <el-tag :type="getAlertTypeTag(scope.row.type)">
                  {{ scope.row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="level" label="等级" width="100">
              <template #default="scope">
                <el-tag :type="getAlertLevelTag(scope.row.level)">
                  {{ scope.row.level }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="content" label="内容" />
          </el-table>
        </el-card>
      </el-col>
      <!-- 待处理漏洞 -->
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>待处理漏洞</span>
            </div>
          </template>
          <el-table :data="pendingVulns" style="width: 100%">
            <el-table-column prop="name" label="漏洞名称" />
            <el-table-column prop="level" label="等级" width="100">
              <template #default="scope">
                <el-tag :type="getVulnLevelTag(scope.row.level)">
                  {{ scope.row.level }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="asset" label="影响资产" width="150" />
            <el-table-column prop="discoveryTime" label="发现时间" width="180" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

// 定义图表引用
const alertTrendChartRef = ref<HTMLElement | null>(null)
const alertTypeChartRef = ref<HTMLElement | null>(null)

const timeRange = ref('7')

// 最新告警数据
const latestAlerts = ref([
  {
    time: '2024-02-20 10:30:00',
    type: '攻击事件',
    level: '高危',
    content: '检测到SSH暴力破解攻击'
  },
  {
    time: '2024-02-20 10:15:00',
    type: '安全事件',
    level: '中危',
    content: '检测到异常登录行为'
  },
  {
    time: '2024-02-20 10:00:00',
    type: '系统事件',
    level: '低危',
    content: '系统资源使用率过高'
  }
])

// 待处理漏洞数据
const pendingVulns = ref([
  {
    name: 'SQL注入漏洞',
    level: '高危',
    asset: 'Web服务器-01',
    discoveryTime: '2024-02-20 09:00:00'
  },
  {
    name: '弱密码',
    level: '中危',
    asset: '数据库服务器-01',
    discoveryTime: '2024-02-20 08:30:00'
  },
  {
    name: '过期证书',
    level: '低危',
    asset: 'Web服务器-02',
    discoveryTime: '2024-02-20 08:00:00'
  }
])

const getAlertTypeTag = (type: string): string => {
  switch (type) {
    case '攻击事件':
      return 'danger'
    case '安全事件':
      return 'warning'
    case '系统事件':
      return 'info'
    default:
      return ''
  }
}

const getAlertLevelTag = (level: string): string => {
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

const getVulnLevelTag = (level: string): string => {
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

onMounted(() => {
  // 初始化告警趋势图
  const alertTrendChart = echarts.init(alertTrendChartRef.value!)
  alertTrendChart.setOption({
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
        name: '告警数量',
        type: 'line',
        data: [15, 12, 8, 10, 14, 9, 12],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })

  // 初始化告警类型分布图
  const alertTypeChart = echarts.init(alertTypeChartRef.value!)
  alertTypeChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '告警类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 35, name: '攻击事件' },
          { value: 25, name: '安全事件' },
          { value: 20, name: '系统事件' },
          { value: 20, name: '其他事件' }
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
}

.score-card,
.alert-card,
.vuln-card,
.asset-card {
  text-align: center;
}

.score-title,
.alert-title,
.vuln-title,
.asset-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.score-value,
.alert-value,
.vuln-value,
.asset-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.score-trend,
.alert-trend,
.vuln-trend,
.asset-trend {
  font-size: 14px;
  color: #909399;
}

.up {
  color: #67c23a;
}

.down {
  color: #f56c6c;
}
</style> 