<template>
  <div class="darkweb-monitor">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>暗网监控</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleScan">开始扫描</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 监控概览 -->
      <div class="monitor-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">今日发现</div>
                <div class="overview-value">12</div>
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
                <div class="overview-title">敏感信息</div>
                <div class="overview-value">8</div>
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
                <div class="overview-title">威胁情报</div>
                <div class="overview-value">15</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    7
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 监控趋势 -->
      <div class="monitor-trend">
        <div class="section-title">监控趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>发现趋势</span>
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
                  <span>信息类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="typeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 监控列表 -->
      <div class="monitor-list">
        <div class="section-title">监控列表</div>
        <el-table :data="monitorList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="type" label="类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="content" label="内容" />
          <el-table-column prop="source" label="来源" width="150" />
          <el-table-column prop="discoveryTime" label="发现时间" width="180" />
          <el-table-column prop="level" label="风险等级" width="100">
            <template #default="scope">
              <el-tag :type="getLevelTag(scope.row.level)">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleBlock(scope.row)">
                封禁
              </el-button>
              <el-button type="warning" link @click="handleTrack(scope.row)">
                追踪
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="监控详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="类型">
            <el-tag :type="getTypeTag(currentItem.type)">
              {{ currentItem.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="来源">{{ currentItem.source }}</el-descriptions-item>
          <el-descriptions-item label="发现时间">{{ currentItem.discoveryTime }}</el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag :type="getLevelTag(currentItem.level)">
              {{ currentItem.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="内容" :span="2">{{ currentItem.content }}</el-descriptions-item>
          <el-descriptions-item label="详细信息" :span="2">{{ currentItem.details }}</el-descriptions-item>
          <el-descriptions-item label="处理建议" :span="2">{{ currentItem.suggestion }}</el-descriptions-item>
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

// 监控列表数据
const monitorList = ref([
  {
    id: 'DARK-2024-001',
    type: '敏感信息',
    content: '发现公司内部邮箱账号密码泄露',
    source: '暗网论坛',
    discoveryTime: '2024-02-20 10:00:00',
    level: '高危',
    details: '在暗网论坛发现公司内部邮箱账号密码信息，涉及多个部门。',
    suggestion: '1. 立即修改相关账号密码\n2. 加强密码策略\n3. 开展安全意识培训',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'warning',
        content: '发现敏感信息泄露'
      },
      {
        time: '2024-02-20 10:15:00',
        type: 'primary',
        content: '开始处理事件'
      }
    ]
  },
  {
    id: 'DARK-2024-002',
    type: '威胁情报',
    content: '发现针对公司的勒索软件攻击计划',
    source: '黑客论坛',
    discoveryTime: '2024-02-20 09:30:00',
    level: '中危',
    details: '在黑客论坛发现针对公司的勒索软件攻击计划，计划在未来一周内实施。',
    suggestion: '1. 加强系统防护\n2. 更新安全策略\n3. 准备应急响应预案',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'warning',
        content: '发现威胁情报'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '敏感信息':
      return 'danger'
    case '威胁情报':
      return 'warning'
    case '漏洞信息':
      return 'info'
    default:
      return ''
  }
}

const getLevelTag = (level: string): string => {
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

const handleScan = () => {
  ElMessage.success('开始暗网扫描...')
}

const handleExport = () => {
  ElMessage.success('导出监控报告...')
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleBlock = (row: any) => {
  ElMessage.success('开始封禁处理...')
}

const handleTrack = (row: any) => {
  ElMessage.success('开始追踪分析...')
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
        name: '发现数量',
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
        name: '信息类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '敏感信息' },
          { value: 30, name: '威胁情报' },
          { value: 20, name: '漏洞信息' },
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
.darkweb-monitor {
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

.monitor-overview {
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

.monitor-trend {
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