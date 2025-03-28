<template>
  <div class="data-backup">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据备份</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleBackup">开始备份</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 备份概览 -->
      <div class="backup-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">待备份数据</div>
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
                <div class="overview-title">已备份数据</div>
                <div class="overview-value">856</div>
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
                <div class="overview-title">备份策略</div>
                <div class="overview-value">5</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    1
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 备份趋势 -->
      <div class="backup-trend">
        <div class="section-title">备份趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>备份数据趋势</span>
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
                  <span>备份类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="typeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 备份列表 -->
      <div class="backup-list">
        <div class="section-title">备份列表</div>
        <el-table :data="backupList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="name" label="数据名称" />
          <el-table-column prop="type" label="备份类型" width="120">
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
          <el-table-column prop="updateTime" label="更新时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleRestore(scope.row)">
                恢复
              </el-button>
              <el-button type="warning" link @click="handleVerify(scope.row)">
                验证
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="备份详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="数据名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="备份类型">
            <el-tag :type="getTypeTag(currentItem.type)">
              {{ currentItem.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTag(currentItem.status)">
              {{ currentItem.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ currentItem.updateTime }}</el-descriptions-item>
          <el-descriptions-item label="操作人">{{ currentItem.operator }}</el-descriptions-item>
          <el-descriptions-item label="备份策略" :span="2">{{ currentItem.policy }}</el-descriptions-item>
          <el-descriptions-item label="存储位置" :span="2">{{ currentItem.location }}</el-descriptions-item>
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
import { ArrowUp } from '@element-plus/icons-vue'

// 定义图表引用
const trendChartRef = ref<HTMLElement | null>(null)
const typeChartRef = ref<HTMLElement | null>(null)

const timeRange = ref('7')

// 备份列表数据
const backupList = ref([
  {
    id: 'BACKUP-2024-001',
    name: '客户数据',
    type: '全量备份',
    status: '待备份',
    updateTime: '2024-02-20 10:00:00',
    operator: 'admin',
    policy: '每周日凌晨2点进行全量备份',
    location: '备份服务器-01',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'primary',
        content: '创建备份任务'
      }
    ]
  },
  {
    id: 'BACKUP-2024-002',
    name: '交易记录',
    type: '增量备份',
    status: '已备份',
    updateTime: '2024-02-20 09:30:00',
    operator: 'admin',
    policy: '每天凌晨1点进行增量备份',
    location: '备份服务器-02',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'success',
        content: '完成备份'
      },
      {
        time: '2024-02-20 09:00:00',
        type: 'primary',
        content: '创建备份任务'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '全量备份':
      return 'danger'
    case '增量备份':
      return 'warning'
    case '差异备份':
      return 'info'
    default:
      return ''
  }
}

const getStatusTag = (status: string): string => {
  switch (status) {
    case '待备份':
      return 'warning'
    case '已备份':
      return 'success'
    case '备份中':
      return 'primary'
    default:
      return ''
  }
}

const handleBackup = () => {
  ElMessage.success('开始数据备份...')
}

const handleExport = () => {
  ElMessage.success('导出备份报告...')
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleRestore = (row: any) => {
  ElMessage.success(`开始恢复数据: ${row.name}`)
}

const handleVerify = (row: any) => {
  ElMessage.success(`开始验证备份: ${row.name}`)
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
        name: '备份数据量',
        type: 'line',
        data: [150, 230, 224, 218, 135, 147, 260],
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
        name: '备份类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '全量备份' },
          { value: 30, name: '增量备份' },
          { value: 20, name: '差异备份' },
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
.data-backup {
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

.backup-overview {
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

.backup-trend {
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