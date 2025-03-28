<template>
  <div class="weight">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>权重管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleSave">保存配置</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleReset">重置默认</el-button>
          </div>
        </div>
      </template>

      <!-- 权重配置 -->
      <div class="weight-config">
        <div class="section-title">评分维度权重配置</div>
        <el-table :data="dimensions" style="width: 100%">
          <el-table-column prop="name" label="维度名称" width="150" />
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="currentWeight" label="当前权重" width="150">
            <template #default="scope">
              <el-input-number
                v-model="scope.row.currentWeight"
                :min="0"
                :max="100"
                :step="5"
                @change="handleWeightChange"
              />
              <span class="weight-unit">%</span>
            </template>
          </el-table-column>
          <el-table-column prop="defaultWeight" label="默认权重" width="100">
            <template #default="scope">
              {{ scope.row.defaultWeight }}%
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>

        <!-- 权重总和提示 -->
        <div class="weight-summary">
          <span>权重总和：</span>
          <span :class="{ 'weight-error': totalWeight !== 100 }">{{ totalWeight }}%</span>
          <el-tag
            v-if="totalWeight !== 100"
            type="danger"
            size="small"
            style="margin-left: 8px"
          >
            权重总和必须为100%
          </el-tag>
        </div>
      </div>

      <!-- 权重调整历史 -->
      <div class="weight-history">
        <div class="section-title">权重调整历史</div>
        <el-table :data="history" style="width: 100%">
          <el-table-column prop="time" label="调整时间" width="180" />
          <el-table-column prop="operator" label="操作人" width="120" />
          <el-table-column prop="dimension" label="调整维度" width="150" />
          <el-table-column prop="oldWeight" label="原权重" width="100">
            <template #default="scope">
              {{ scope.row.oldWeight }}%
            </template>
          </el-table-column>
          <el-table-column prop="newWeight" label="新权重" width="100">
            <template #default="scope">
              {{ scope.row.newWeight }}%
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="调整原因" />
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleRollback(scope.row)">
                回滚
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 权重影响分析 -->
      <div class="weight-impact">
        <div class="section-title">权重调整影响分析</div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>评分影响</span>
                </div>
              </template>
              <div class="chart-container" ref="scoreImpactChartRef"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>维度贡献变化</span>
                </div>
              </template>
              <div class="chart-container" ref="contributionChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import * as echarts from 'echarts'

const dimensions = ref([
  {
    name: '资产安全',
    description: '资产发现、分类、风险评估等',
    currentWeight: 30,
    defaultWeight: 30,
    status: '已修改'
  },
  {
    name: '漏洞管理',
    description: '漏洞扫描、修复、验证等',
    currentWeight: 25,
    defaultWeight: 25,
    status: '已修改'
  },
  {
    name: '安全事件',
    description: '事件检测、响应、处置等',
    currentWeight: 20,
    defaultWeight: 20,
    status: '正常'
  },
  {
    name: '合规管理',
    description: '合规检查、基线核查等',
    currentWeight: 15,
    defaultWeight: 15,
    status: '正常'
  },
  {
    name: '安全运营',
    description: '安全运营、运维管理等',
    currentWeight: 10,
    defaultWeight: 10,
    status: '正常'
  }
])

const history = ref([
  {
    time: '2024-02-20 10:00:00',
    operator: 'admin',
    dimension: '资产安全',
    oldWeight: 25,
    newWeight: 30,
    reason: '提升资产安全管理重要性'
  },
  {
    time: '2024-02-20 09:30:00',
    operator: 'admin',
    dimension: '漏洞管理',
    oldWeight: 30,
    newWeight: 25,
    reason: '调整漏洞管理权重'
  }
])

const totalWeight = computed(() => {
  return dimensions.value.reduce((sum, item) => sum + item.currentWeight, 0)
})

const getStatusType = (status: string): string => {
  switch (status) {
    case '已修改':
      return 'warning'
    case '正常':
      return 'success'
    default:
      return 'info'
  }
}

const handleWeightChange = () => {
  // 更新状态
  dimensions.value.forEach(item => {
    if (item.currentWeight !== item.defaultWeight) {
      item.status = '已修改'
    } else {
      item.status = '正常'
    }
  })
}

const handleSave = () => {
  if (totalWeight.value !== 100) {
    ElMessage.error('权重总和必须为100%')
    return
  }
  // TODO: 保存配置
  ElMessage.success('保存成功')
}

const handleReset = () => {
  dimensions.value.forEach(item => {
    item.currentWeight = item.defaultWeight
    item.status = '正常'
  })
}

const handleRollback = (row: any) => {
  const dimension = dimensions.value.find(d => d.name === row.dimension)
  if (dimension) {
    dimension.currentWeight = row.oldWeight
    dimension.status = dimension.currentWeight === dimension.defaultWeight ? '正常' : '已修改'
  }
}

onMounted(() => {
  // 初始化评分影响图
  const scoreImpactChart = echarts.init(scoreImpactChartRef.value!)
  scoreImpactChart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['调整前', '调整后']
    },
    xAxis: {
      type: 'category',
      data: ['资产安全', '漏洞管理', '安全事件', '合规管理', '安全运营']
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100
    },
    series: [
      {
        name: '调整前',
        type: 'bar',
        data: [85, 82, 78, 90, 88]
      },
      {
        name: '调整后',
        type: 'bar',
        data: [88, 80, 78, 90, 88]
      }
    ]
  })

  // 初始化维度贡献变化图
  const contributionChart = echarts.init(contributionChartRef.value!)
  contributionChart.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '维度贡献',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 26.4, name: '资产安全' },
          { value: 20, name: '漏洞管理' },
          { value: 15.6, name: '安全事件' },
          { value: 13.2, name: '合规管理' },
          { value: 8.8, name: '安全运营' }
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
.weight {
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

.weight-unit {
  margin-left: 4px;
  color: #909399;
}

.weight-summary {
  margin-top: 16px;
  text-align: right;
  font-size: 14px;
}

.weight-error {
  color: #f56c6c;
  font-weight: bold;
}

.weight-history {
  margin-top: 40px;
}

.weight-impact {
  margin-top: 40px;
}

.chart-container {
  height: 300px;
}
</style> 