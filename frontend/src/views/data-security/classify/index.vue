<template>
  <div class="data-classify">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据分类</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleScan">开始扫描</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 分类概览 -->
      <div class="classify-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">敏感数据</div>
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
                <div class="overview-title">个人数据</div>
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
                <div class="overview-title">业务数据</div>
                <div class="overview-value">2,345</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    156
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 分类趋势 -->
      <div class="classify-trend">
        <div class="section-title">分类趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>数据分类趋势</span>
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
                  <span>数据分类分布</span>
                </div>
              </template>
              <div class="chart-container" ref="typeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 分类列表 -->
      <div class="classify-list">
        <div class="section-title">分类列表</div>
        <el-table :data="classifyList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="name" label="数据名称" />
          <el-table-column prop="type" label="数据类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="level" label="敏感等级" width="100">
            <template #default="scope">
              <el-tag :type="getLevelTag(scope.row.level)">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="location" label="存储位置" width="150" />
          <el-table-column prop="updateTime" label="更新时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleProtect(scope.row)">
                保护
              </el-button>
              <el-button type="warning" link @click="handleAudit(scope.row)">
                审计
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="分类详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="数据名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="数据类型">
            <el-tag :type="getTypeTag(currentItem.type)">
              {{ currentItem.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="敏感等级">
            <el-tag :type="getLevelTag(currentItem.level)">
              {{ currentItem.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="存储位置">{{ currentItem.location }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ currentItem.updateTime }}</el-descriptions-item>
          <el-descriptions-item label="数据描述" :span="2">{{ currentItem.description }}</el-descriptions-item>
          <el-descriptions-item label="保护措施" :span="2">{{ currentItem.protection }}</el-descriptions-item>
          <el-descriptions-item label="访问记录" :span="2">
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

// 分类列表数据
const classifyList = ref([
  {
    id: 'DATA-2024-001',
    name: '客户信息表',
    type: '个人数据',
    level: '高',
    location: '数据库服务器-01',
    updateTime: '2024-02-20 10:00:00',
    description: '包含客户基本信息、联系方式等敏感信息。',
    protection: '1. 数据加密存储\n2. 访问权限控制\n3. 操作审计',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'primary',
        content: '更新数据分类'
      },
      {
        time: '2024-02-20 09:30:00',
        type: 'success',
        content: '应用保护措施'
      }
    ]
  },
  {
    id: 'DATA-2024-002',
    name: '财务数据',
    type: '业务数据',
    level: '中',
    location: '文件服务器-02',
    updateTime: '2024-02-20 09:30:00',
    description: '包含公司财务相关数据，需要定期备份。',
    protection: '1. 定期备份\n2. 访问控制\n3. 数据脱敏',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'primary',
        content: '更新数据分类'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '个人数据':
      return 'danger'
    case '业务数据':
      return 'warning'
    case '系统数据':
      return 'info'
    default:
      return ''
  }
}

const getLevelTag = (level: string): string => {
  switch (level) {
    case '高':
      return 'danger'
    case '中':
      return 'warning'
    case '低':
      return 'info'
    default:
      return ''
  }
}

const handleScan = () => {
  ElMessage.success('开始数据扫描...')
}

const handleExport = () => {
  ElMessage.success('导出分类报告...')
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleProtect = (row: any) => {
  ElMessage.success(`开始保护数据: ${row.name}`)
}

const handleAudit = (row: any) => {
  ElMessage.success(`开始审计数据: ${row.name}`)
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
        name: '数据量',
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
        name: '数据类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '个人数据' },
          { value: 30, name: '业务数据' },
          { value: 20, name: '系统数据' },
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
.data-classify {
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

.classify-overview {
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

.classify-trend {
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