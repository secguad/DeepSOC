<template>
  <div class="inventory">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>资产清单</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAdd">添加资产</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出清单</el-button>
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
                  <span>资产状态分布</span>
                </div>
              </template>
              <div class="chart-container" ref="assetStatusChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 资产列表 -->
      <div class="asset-list">
        <div class="section-title">资产列表</div>
        <el-table :data="assetList" style="width: 100%">
          <el-table-column prop="id" label="资产ID" width="120" />
          <el-table-column prop="name" label="资产名称" width="200" />
          <el-table-column prop="type" label="资产类型" width="120">
            <template #default="scope">
              <el-tag :type="getAssetTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="ip" label="IP地址" width="150" />
          <el-table-column prop="os" label="操作系统" width="150" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getAssetStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="lastScanTime" label="最后扫描时间" width="180" />
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleScan(scope.row)">
                扫描
              </el-button>
              <el-button type="warning" link @click="handleEdit(scope.row)">
                编辑
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
          <el-descriptions-item label="资产ID">{{ currentAsset.id }}</el-descriptions-item>
          <el-descriptions-item label="资产名称">{{ currentAsset.name }}</el-descriptions-item>
          <el-descriptions-item label="资产类型">
            <el-tag :type="getAssetTypeTag(currentAsset.type)">
              {{ currentAsset.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getAssetStatusTag(currentAsset.status)">
              {{ currentAsset.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="IP地址">{{ currentAsset.ip }}</el-descriptions-item>
          <el-descriptions-item label="操作系统">{{ currentAsset.os }}</el-descriptions-item>
          <el-descriptions-item label="MAC地址">{{ currentAsset.mac }}</el-descriptions-item>
          <el-descriptions-item label="所属部门">{{ currentAsset.department }}</el-descriptions-item>
          <el-descriptions-item label="负责人">{{ currentAsset.owner }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentAsset.createTime }}</el-descriptions-item>
          <el-descriptions-item label="最后扫描时间">{{ currentAsset.lastScanTime }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ currentAsset.remark }}</el-descriptions-item>
          <el-descriptions-item label="开放端口" :span="2">
            <el-tag
              v-for="port in currentAsset.ports"
              :key="port"
              style="margin-right: 8px; margin-bottom: 8px"
            >
              {{ port }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="运行服务" :span="2">
            <el-tag
              v-for="service in currentAsset.services"
              :key="service"
              type="success"
              style="margin-right: 8px; margin-bottom: 8px"
            >
              {{ service }}
            </el-tag>
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
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

// 定义图表引用
const assetTypeChartRef = ref<HTMLElement | null>(null)
const assetStatusChartRef = ref<HTMLElement | null>(null)

// 定义资产类型接口
interface Asset {
  id: string
  name: string
  type: string
  ip: string
  os: string
  status: string
  mac: string
  department: string
  owner: string
  createTime: string
  lastScanTime: string
  remark: string
  ports: number[]
  services: string[]
}

const overview = ref([
  {
    title: '总资产数',
    value: '156',
    trend: 5
  },
  {
    title: '在线资产',
    value: '142',
    trend: 3
  },
  {
    title: '离线资产',
    value: '14',
    trend: -10
  },
  {
    title: '新增资产',
    value: '8',
    trend: 20
  }
])

const assetList = ref<Asset[]>([
  {
    id: 'ASSET-2024-001',
    name: 'Web服务器-01',
    type: '服务器',
    ip: '192.168.1.100',
    os: 'CentOS 7.9',
    status: '在线',
    mac: '00:11:22:33:44:55',
    department: '研发部',
    owner: '张三',
    createTime: '2024-01-01 10:00:00',
    lastScanTime: '2024-02-20 10:00:00',
    remark: '生产环境Web服务器',
    ports: [80, 443, 22, 3306],
    services: ['nginx', 'mysql', 'sshd']
  },
  {
    id: 'ASSET-2024-002',
    name: '数据库服务器-01',
    type: '服务器',
    ip: '192.168.1.101',
    os: 'Ubuntu 20.04',
    status: '在线',
    mac: '00:11:22:33:44:66',
    department: '运维部',
    owner: '李四',
    createTime: '2024-01-02 14:00:00',
    lastScanTime: '2024-02-20 09:00:00',
    remark: '生产环境数据库服务器',
    ports: [3306, 5432, 22],
    services: ['mysql', 'postgresql', 'sshd']
  }
])

const detailVisible = ref(false)
const currentAsset = ref<Asset | null>(null)

const getAssetTypeTag = (type: string): string => {
  switch (type) {
    case '服务器':
      return 'primary'
    case '网络设备':
      return 'success'
    case '安全设备':
      return 'warning'
    case '终端设备':
      return 'info'
    default:
      return ''
  }
}

const getAssetStatusTag = (status: string): string => {
  switch (status) {
    case '在线':
      return 'success'
    case '离线':
      return 'danger'
    case '维护中':
      return 'warning'
    default:
      return ''
  }
}

const handleAdd = () => {
  ElMessage.success('添加新资产...')
}

const handleExport = () => {
  ElMessage.success('导出资产清单...')
}

const handleDetail = (row: Asset) => {
  currentAsset.value = row
  detailVisible.value = true
}

const handleScan = (row: Asset) => {
  ElMessage.success(`开始扫描资产：${row.name}`)
}

const handleEdit = (row: Asset) => {
  ElMessage.success(`编辑资产：${row.name}`)
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
          { value: 80, name: '服务器' },
          { value: 30, name: '网络设备' },
          { value: 20, name: '安全设备' },
          { value: 26, name: '终端设备' }
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

  // 初始化资产状态分布图
  const assetStatusChart = echarts.init(assetStatusChartRef.value!)
  assetStatusChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '资产状态',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 142, name: '在线' },
          { value: 14, name: '离线' },
          { value: 5, name: '维护中' }
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
.inventory {
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