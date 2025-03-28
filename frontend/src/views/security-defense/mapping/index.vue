<template>
  <div class="mapping">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>互联网攻击面测绘</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleScan">开始扫描</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 资产概览 -->
      <div class="asset-overview">
        <el-row :gutter="20">
          <el-col :span="6" v-for="(item, index) in overview" :key="index">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">{{ item.title }}</div>
                <div class="overview-value">{{ item.value }}</div>
                <div class="overview-trend">
                  较上期
                  <span :class="item.trend >= 0 ? 'up' : 'down'">
                    {{ Math.abs(item.trend) }}%
                    <el-icon>
                      <component :is="item.trend >= 0 ? 'ArrowUp' : 'ArrowDown'" />
                    </el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 资产分布 -->
      <div class="asset-distribution">
        <div class="section-title">资产分布</div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>资产类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="assetTypeChartRef"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>资产地理位置分布</span>
                </div>
              </template>
              <div class="chart-container" ref="assetLocationChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 资产列表 -->
      <div class="asset-list">
        <div class="section-title">资产列表</div>
        <el-table :data="assetList" style="width: 100%">
          <el-table-column prop="name" label="资产名称" width="150" />
          <el-table-column prop="type" label="资产类型" width="120">
            <template #default="scope">
              <el-tag :type="getAssetTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="ip" label="IP地址" width="150" />
          <el-table-column prop="domain" label="域名" width="200" />
          <el-table-column prop="location" label="地理位置" width="150" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getAssetStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="lastScanTime" label="最后扫描时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleScanAsset(scope.row)">
                扫描
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 资产详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="资产详情"
      width="800px"
    >
      <div v-if="currentAsset" class="asset-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="资产名称">{{ currentAsset.name }}</el-descriptions-item>
          <el-descriptions-item label="资产类型">
            <el-tag :type="getAssetTypeTag(currentAsset.type)">
              {{ currentAsset.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="IP地址">{{ currentAsset.ip }}</el-descriptions-item>
          <el-descriptions-item label="域名">{{ currentAsset.domain }}</el-descriptions-item>
          <el-descriptions-item label="地理位置">{{ currentAsset.location }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getAssetStatusTag(currentAsset.status)">
              {{ currentAsset.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="开放端口" :span="2">{{ currentAsset.ports }}</el-descriptions-item>
          <el-descriptions-item label="运行服务" :span="2">{{ currentAsset.services }}</el-descriptions-item>
          <el-descriptions-item label="发现时间">{{ currentAsset.discoveryTime }}</el-descriptions-item>
          <el-descriptions-item label="最后扫描时间">{{ currentAsset.lastScanTime }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ currentAsset.remark }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

const overview = ref([
  {
    title: '总资产数',
    value: '156',
    trend: 5
  },
  {
    title: '新增资产',
    value: '8',
    trend: 20
  },
  {
    title: '高危资产',
    value: '12',
    trend: -10
  },
  {
    title: '待处理',
    value: '5',
    trend: -20
  }
])

const assetList = ref([
  {
    name: 'Web服务器-01',
    type: 'Web服务器',
    ip: '192.168.1.100',
    domain: 'www.example.com',
    location: '北京',
    status: '正常',
    lastScanTime: '2024-02-20 10:00:00',
    ports: '80,443,8080',
    services: 'Nginx,MySQL,Redis',
    discoveryTime: '2024-01-01 00:00:00',
    remark: '主站服务器'
  },
  {
    name: '数据库服务器-01',
    type: '数据库服务器',
    ip: '192.168.1.101',
    domain: 'db.example.com',
    location: '上海',
    status: '异常',
    lastScanTime: '2024-02-20 09:30:00',
    ports: '3306,6379',
    services: 'MySQL,Redis',
    discoveryTime: '2024-01-01 00:00:00',
    remark: '主数据库服务器'
  }
])

const detailVisible = ref(false)
const currentAsset = ref(null)

const getAssetTypeTag = (type: string): string => {
  switch (type) {
    case 'Web服务器':
      return 'primary'
    case '数据库服务器':
      return 'success'
    case '应用服务器':
      return 'warning'
    default:
      return 'info'
  }
}

const getAssetStatusTag = (status: string): string => {
  switch (status) {
    case '正常':
      return 'success'
    case '异常':
      return 'danger'
    case '维护中':
      return 'warning'
    default:
      return 'info'
  }
}

const handleScan = () => {
  ElMessage.success('开始扫描资产...')
}

const handleExport = () => {
  ElMessage.success('导出报告...')
}

const handleDetail = (row: any) => {
  currentAsset.value = row
  detailVisible.value = true
}

const handleScanAsset = (row: any) => {
  ElMessage.success(`开始扫描资产：${row.name}`)
}

onMounted(() => {
  // 初始化资产类型分布图
  const assetTypeChart = echarts.init(assetTypeChartRef.value!)
  assetTypeChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '资产类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 45, name: 'Web服务器' },
          { value: 25, name: '数据库服务器' },
          { value: 20, name: '应用服务器' },
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

  // 初始化资产地理位置分布图
  const assetLocationChart = echarts.init(assetLocationChartRef.value!)
  assetLocationChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '地理位置',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 40, name: '北京' },
          { value: 30, name: '上海' },
          { value: 20, name: '广州' },
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
.mapping {
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

.asset-overview {
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

.asset-distribution {
  margin-bottom: 40px;
}

.chart-container {
  height: 300px;
}

.asset-detail {
  padding: 20px;
}
</style> 