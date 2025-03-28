<template>
  <div class="intelligence">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>漏洞情报</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleRefresh">刷新情报</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleSubscribe">订阅配置</el-button>
          </div>
        </div>
      </template>

      <!-- 情报概览 -->
      <div class="intelligence-overview">
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

      <!-- 漏洞趋势 -->
      <div class="vuln-trend">
        <div class="section-title">漏洞趋势</div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>漏洞数量趋势</span>
                  <el-select v-model="timeRange" size="small">
                    <el-option label="近7天" value="7" />
                    <el-option label="近30天" value="30" />
                    <el-option label="近90天" value="90" />
                  </el-select>
                </div>
              </template>
              <div class="chart-container" ref="vulnCountChartRef"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>漏洞类型分布</span>
                </div>
              </template>
              <div class="chart-container" ref="vulnTypeChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 漏洞列表 -->
      <div class="vuln-list">
        <div class="section-title">最新漏洞</div>
        <el-table :data="vulnList" style="width: 100%">
          <el-table-column prop="id" label="漏洞ID" width="120" />
          <el-table-column prop="name" label="漏洞名称" width="200" />
          <el-table-column prop="type" label="漏洞类型" width="120">
            <template #default="scope">
              <el-tag :type="getVulnTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="level" label="危险等级" width="100">
            <template #default="scope">
              <el-tag :type="getVulnLevelTag(scope.row.level)">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="source" label="情报来源" width="120" />
          <el-table-column prop="publishTime" label="发布时间" width="180" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getVulnStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleVerify(scope.row)">
                验证
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 漏洞详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="漏洞详情"
      width="800px"
    >
      <div v-if="currentVuln" class="vuln-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="漏洞ID">{{ currentVuln.id }}</el-descriptions-item>
          <el-descriptions-item label="漏洞名称">{{ currentVuln.name }}</el-descriptions-item>
          <el-descriptions-item label="漏洞类型">
            <el-tag :type="getVulnTypeTag(currentVuln.type)">
              {{ currentVuln.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="危险等级">
            <el-tag :type="getVulnLevelTag(currentVuln.level)">
              {{ currentVuln.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="情报来源">{{ currentVuln.source }}</el-descriptions-item>
          <el-descriptions-item label="发布时间">{{ currentVuln.publishTime }}</el-descriptions-item>
          <el-descriptions-item label="CVE编号" :span="2">{{ currentVuln.cve }}</el-descriptions-item>
          <el-descriptions-item label="漏洞描述" :span="2">{{ currentVuln.description }}</el-descriptions-item>
          <el-descriptions-item label="影响范围" :span="2">{{ currentVuln.scope }}</el-descriptions-item>
          <el-descriptions-item label="修复建议" :span="2">{{ currentVuln.solution }}</el-descriptions-item>
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
    title: '今日新增',
    value: '12',
    trend: 20
  },
  {
    title: '高危漏洞',
    value: '5',
    trend: -10
  },
  {
    title: '已修复',
    value: '8',
    trend: 15
  },
  {
    title: '待处理',
    value: '4',
    trend: -20
  }
])

const timeRange = ref('7')

const vulnList = ref([
  {
    id: 'VULN-2024-001',
    name: 'Apache Log4j 远程代码执行漏洞',
    type: '远程代码执行',
    level: '高危',
    source: 'CVE',
    publishTime: '2024-02-20 10:00:00',
    status: '待验证',
    cve: 'CVE-2024-0001',
    description: 'Apache Log4j 2.x版本存在远程代码执行漏洞，攻击者可利用该漏洞在目标服务器上执行任意代码。',
    scope: 'Apache Log4j 2.0.0 - 2.14.0',
    solution: '升级到Log4j 2.15.0或更高版本'
  },
  {
    id: 'VULN-2024-002',
    name: 'Spring Framework 反序列化漏洞',
    type: '反序列化',
    level: '高危',
    source: 'CVE',
    publishTime: '2024-02-20 09:30:00',
    status: '已验证',
    cve: 'CVE-2024-0002',
    description: 'Spring Framework 5.3.x版本存在反序列化漏洞，攻击者可利用该漏洞实现远程代码执行。',
    scope: 'Spring Framework 5.3.0 - 5.3.20',
    solution: '升级到Spring Framework 5.3.21或更高版本'
  }
])

const detailVisible = ref(false)
const currentVuln = ref(null)

const getVulnTypeTag = (type: string): string => {
  switch (type) {
    case '远程代码执行':
      return 'danger'
    case '反序列化':
      return 'warning'
    default:
      return 'info'
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

const getVulnStatusTag = (status: string): string => {
  switch (status) {
    case '待验证':
      return 'warning'
    case '已验证':
      return 'success'
    case '已修复':
      return 'info'
    default:
      return ''
  }
}

const handleRefresh = () => {
  ElMessage.success('正在刷新漏洞情报...')
}

const handleSubscribe = () => {
  ElMessage.success('打开订阅配置...')
}

const handleDetail = (row: any) => {
  currentVuln.value = row
  detailVisible.value = true
}

const handleVerify = (row: any) => {
  ElMessage.success('开始验证漏洞...')
}

onMounted(() => {
  // 初始化漏洞数量趋势图
  const vulnCountChart = echarts.init(vulnCountChartRef.value!)
  vulnCountChart.setOption({
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
        name: '漏洞数量',
        type: 'line',
        data: [5, 8, 3, 9, 6, 10, 12],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })

  // 初始化漏洞类型分布图
  const vulnTypeChart = echarts.init(vulnTypeChartRef.value!)
  vulnTypeChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '漏洞类型',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 35, name: '远程代码执行' },
          { value: 25, name: '反序列化' },
          { value: 20, name: 'SQL注入' },
          { value: 15, name: 'XSS' },
          { value: 5, name: '其他' }
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
.intelligence {
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

.intelligence-overview {
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

.vuln-trend {
  margin-bottom: 40px;
}

.chart-container {
  height: 300px;
}

.vuln-detail {
  padding: 20px;
}
</style> 