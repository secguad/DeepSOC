<template>
  <div class="data-encrypt">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据加密</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleScan">开始扫描</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 加密概览 -->
      <div class="encrypt-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">待加密数据</div>
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
                <div class="overview-title">已加密数据</div>
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
                <div class="overview-title">加密算法</div>
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

      <!-- 加密趋势 -->
      <div class="encrypt-trend">
        <div class="section-title">加密趋势</div>
        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>加密数据趋势</span>
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
                  <span>加密算法分布</span>
                </div>
              </template>
              <div class="chart-container" ref="typeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 加密列表 -->
      <div class="encrypt-list">
        <div class="section-title">加密列表</div>
        <el-table :data="encryptList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="name" label="数据名称" />
          <el-table-column prop="algorithm" label="加密算法" width="120">
            <template #default="scope">
              <el-tag :type="getAlgorithmTag(scope.row.algorithm)">
                {{ scope.row.algorithm }}
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
              <el-button type="success" link @click="handleEncrypt(scope.row)">
                加密
              </el-button>
              <el-button type="warning" link @click="handleDecrypt(scope.row)">
                解密
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="加密详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="数据名称">{{ currentItem.name }}</el-descriptions-item>
          <el-descriptions-item label="加密算法">
            <el-tag :type="getAlgorithmTag(currentItem.algorithm)">
              {{ currentItem.algorithm }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTag(currentItem.status)">
              {{ currentItem.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ currentItem.updateTime }}</el-descriptions-item>
          <el-descriptions-item label="操作人">{{ currentItem.operator }}</el-descriptions-item>
          <el-descriptions-item label="密钥信息" :span="2">{{ currentItem.keyInfo }}</el-descriptions-item>
          <el-descriptions-item label="加密参数" :span="2">{{ currentItem.params }}</el-descriptions-item>
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

// 加密列表数据
const encryptList = ref([
  {
    id: 'ENCRYPT-2024-001',
    name: '客户密码',
    algorithm: 'AES-256',
    status: '待加密',
    updateTime: '2024-02-20 10:00:00',
    operator: 'admin',
    keyInfo: '使用AES-256-GCM模式，密钥长度256位',
    params: 'IV长度：12字节\n认证标签长度：16字节',
    activities: [
      {
        time: '2024-02-20 10:00:00',
        type: 'primary',
        content: '创建加密任务'
      }
    ]
  },
  {
    id: 'ENCRYPT-2024-002',
    name: '支付信息',
    algorithm: 'RSA-2048',
    status: '已加密',
    updateTime: '2024-02-20 09:30:00',
    operator: 'admin',
    keyInfo: '使用RSA-2048，公钥加密',
    params: '填充方式：PKCS1\n哈希算法：SHA-256',
    activities: [
      {
        time: '2024-02-20 09:30:00',
        type: 'success',
        content: '完成加密'
      },
      {
        time: '2024-02-20 09:00:00',
        type: 'primary',
        content: '创建加密任务'
      }
    ]
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getAlgorithmTag = (algorithm: string): string => {
  switch (algorithm) {
    case 'AES-256':
      return 'danger'
    case 'RSA-2048':
      return 'warning'
    case 'SM4':
      return 'info'
    default:
      return ''
  }
}

const getStatusTag = (status: string): string => {
  switch (status) {
    case '待加密':
      return 'warning'
    case '已加密':
      return 'success'
    case '加密中':
      return 'primary'
    default:
      return ''
  }
}

const handleScan = () => {
  ElMessage.success('开始数据扫描...')
}

const handleExport = () => {
  ElMessage.success('导出加密报告...')
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleEncrypt = (row: any) => {
  ElMessage.success(`开始加密数据: ${row.name}`)
}

const handleDecrypt = (row: any) => {
  ElMessage.success(`开始解密数据: ${row.name}`)
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
        name: '加密数据量',
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
        name: '加密算法',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: 'AES-256' },
          { value: 30, name: 'RSA-2048' },
          { value: 20, name: 'SM4' },
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
.data-encrypt {
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

.encrypt-overview {
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

.encrypt-trend {
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