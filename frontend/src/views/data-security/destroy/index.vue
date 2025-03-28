<template>
  <div class="data-destroy">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据销毁</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleDestroy">开始销毁</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 销毁概览 -->
      <div class="destroy-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">待销毁数据</div>
                <div class="overview-value">123</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    12
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">已销毁数据</div>
                <div class="overview-value">89</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    8
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">销毁策略</div>
                <div class="overview-value">3</div>
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

      <!-- 销毁趋势 -->
      <div class="destroy-trend">
        <div class="section-title">销毁趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>销毁数据趋势</span>
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
                  <span>销毁类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="typeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 销毁列表 -->
      <div class="destroy-list">
        <div class="section-title">销毁列表</div>
        <el-table :data="destroyList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="name" label="数据名称" />
          <el-table-column prop="type" label="销毁类型" width="120">
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
              <el-button type="danger" link @click="handleDestroy(scope.row)">
                销毁
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
      title="销毁详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="数据名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="销毁类型">
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
          <el-descriptions-item label="销毁策略" :span="2">{{ currentItem.policy }}</el-descriptions-item>
          <el-descriptions-item label="销毁原因" :span="2">{{ currentItem.reason }}</el-descriptions-item>
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

// 销毁列表数据
const destroyList = ref([
  {
    id: 'DESTROY-2024-001',
    name: '过期客户数据',
    type: '物理销毁',
    status: '待销毁',
    updateTime: '2024-02-20 10:00:00',
    operator: 'admin',
    policy: '使用物理销毁设备进行数据销毁',
    reason: '数据已过期，需要销毁',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'primary',
        content: '创建销毁任务'
      }
    ]
  },
  {
    id: 'DESTROY-2024-002',
    name: '临时文件',
    type: '逻辑销毁',
    status: '已销毁',
    updateTime: '2024-02-20 09:30:00',
    operator: 'admin',
    policy: '使用安全擦除算法进行数据销毁',
    reason: '临时文件清理',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'success',
        content: '完成销毁'
      },
      {
        time: '2024-02-20 09:00:00',
        type: 'primary',
        content: '创建销毁任务'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '物理销毁':
      return 'danger'
    case '逻辑销毁':
      return 'warning'
    case '加密销毁':
      return 'info'
    default:
      return ''
  }
}

const getStatusTag = (status: string): string => {
  switch (status) {
    case '待销毁':
      return 'warning'
    case '已销毁':
      return 'success'
    case '销毁中':
      return 'primary'
    default:
      return ''
  }
}

const handleDestroy = (row: any) => {
  ElMessage.success(`开始销毁数据: ${row.name}`)
}

const handleExport = () => {
  ElMessage.success('导出销毁报告...')
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleVerify = (row: any) => {
  ElMessage.success(`开始验证销毁: ${row.name}`)
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
        name: '销毁数据量',
        type: 'line',
        data: [15, 23, 22, 21, 13, 14, 26],
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
        name: '销毁类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '物理销毁' },
          { value: 30, name: '逻辑销毁' },
          { value: 20, name: '加密销毁' },
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
.data-destroy {
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

.destroy-overview {
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

.destroy-trend {
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