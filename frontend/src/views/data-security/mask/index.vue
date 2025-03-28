<template>
  <div class="data-mask">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据脱敏</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleScan">开始扫描</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 脱敏概览 -->
      <div class="mask-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">待脱敏数据</div>
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
                <div class="overview-title">已脱敏数据</div>
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
                <div class="overview-title">脱敏规则</div>
                <div class="overview-value">12</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    2
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 脱敏趋势 -->
      <div class="mask-trend">
        <div class="section-title">脱敏趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>脱敏数据趋势</span>
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
                  <span>脱敏类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="typeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 脱敏列表 -->
      <div class="mask-list">
        <div class="section-title">脱敏列表</div>
        <el-table :data="maskList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="name" label="数据名称" />
          <el-table-column prop="type" label="脱敏类型" width="120">
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
              <el-button type="success" link @click="handleMask(scope.row)">
                脱敏
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
      title="脱敏详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="数据名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="脱敏类型">
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
          <el-descriptions-item label="脱敏规则" :span="2">{{ currentItem.rule }}</el-descriptions-item>
          <el-descriptions-item label="脱敏效果" :span="2">{{ currentItem.effect }}</el-descriptions-item>
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

// 脱敏列表数据
const maskList = ref([
  {
    id: 'MASK-2024-001',
    name: '客户手机号',
    type: '手机号脱敏',
    status: '待脱敏',
    updateTime: '2024-02-20 10:00:00',
    operator: 'admin',
    rule: '保留前3位和后4位，中间用*代替',
    effect: '138****8888',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'primary',
        content: '创建脱敏任务'
      }
    ]
  },
  {
    id: 'MASK-2024-002',
    name: '身份证号',
    type: '身份证脱敏',
    status: '已脱敏',
    updateTime: '2024-02-20 09:30:00',
    operator: 'admin',
    rule: '保留前6位和后4位，中间用*代替',
    effect: '110101****8888',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'success',
        content: '完成脱敏'
      },
      {
        time: '2024-02-20 09:00:00',
        type: 'primary',
        content: '创建脱敏任务'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '手机号脱敏':
      return 'danger'
    case '身份证脱敏':
      return 'warning'
    case '邮箱脱敏':
      return 'info'
    default:
      return ''
  }
}

const getStatusTag = (status: string): string => {
  switch (status) {
    case '待脱敏':
      return 'warning'
    case '已脱敏':
      return 'success'
    case '脱敏中':
      return 'primary'
    default:
      return ''
  }
}

const handleScan = () => {
  ElMessage.success('开始数据扫描...')
}

const handleExport = () => {
  ElMessage.success('导出脱敏报告...')
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleMask = (row: any) => {
  ElMessage.success(`开始脱敏数据: ${row.name}`)
}

const handleVerify = (row: any) => {
  ElMessage.success(`开始验证数据: ${row.name}`)
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
        name: '脱敏数据量',
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
        name: '脱敏类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '手机号脱敏' },
          { value: 30, name: '身份证脱敏' },
          { value: 20, name: '邮箱脱敏' },
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
.data-mask {
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

.mask-overview {
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

.mask-trend {
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