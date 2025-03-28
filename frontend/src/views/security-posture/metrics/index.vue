<template>
  <div class="metrics">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>运营指标维护</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleSave">保存配置</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleAdd">添加指标</el-button>
          </div>
        </div>
      </template>

      <!-- 指标配置 -->
      <div class="metrics-config">
        <div class="section-title">指标配置</div>
        <el-table :data="metrics" style="width: 100%">
          <el-table-column prop="name" label="指标名称" width="150" />
          <el-table-column prop="code" label="指标代码" width="120" />
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="unit" label="单位" width="100" />
          <el-table-column prop="weight" label="权重" width="100">
            <template #default="scope">
              {{ scope.row.weight }}%
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleEdit(scope.row)">
                编辑
              </el-button>
              <el-button type="danger" link @click="handleDelete(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 指标趋势 -->
      <div class="metrics-trend">
        <div class="section-title">指标趋势</div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>安全事件响应时间趋势</span>
                  <el-select v-model="timeRange" size="small">
                    <el-option label="近7天" value="7" />
                    <el-option label="近30天" value="30" />
                    <el-option label="近90天" value="90" />
                  </el-select>
                </div>
              </template>
              <div class="chart-container" ref="responseTimeChartRef"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>漏洞修复率趋势</span>
                </div>
              </template>
              <div class="chart-container" ref="fixRateChartRef"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 指标分析 -->
      <div class="metrics-analysis">
        <div class="section-title">指标分析</div>
        <el-row :gutter="20">
          <el-col :span="8" v-for="(item, index) in analysis" :key="index">
            <el-card shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>{{ item.title }}</span>
                </div>
              </template>
              <div class="analysis-content">
                <div class="analysis-value">{{ item.value }}</div>
                <div class="analysis-compare">
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
    </el-card>

    <!-- 添加/编辑指标对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加指标' : '编辑指标'"
      width="500px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="指标名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="指标代码">
          <el-input v-model="form.code" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="form.description" />
        </el-form-item>
        <el-form-item label="单位">
          <el-input v-model="form.unit" />
        </el-form-item>
        <el-form-item label="权重">
          <el-input-number v-model="form.weight" :min="0" :max="100" />
          <span class="weight-unit">%</span>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

const metrics = ref([
  {
    name: '安全事件响应时间',
    code: 'SEC_RESP_TIME',
    description: '从安全事件发生到开始处理的时间',
    unit: '分钟',
    weight: 20,
    status: '正常'
  },
  {
    name: '漏洞修复率',
    code: 'VULN_FIX_RATE',
    description: '已修复漏洞数量占总漏洞数量的比例',
    unit: '%',
    weight: 25,
    status: '正常'
  },
  {
    name: '安全基线符合率',
    code: 'BASE_COMP_RATE',
    description: '符合安全基线的资产数量占总资产数量的比例',
    unit: '%',
    weight: 15,
    status: '正常'
  },
  {
    name: '安全事件处理率',
    code: 'SEC_HANDLE_RATE',
    description: '已处理安全事件数量占总安全事件数量的比例',
    unit: '%',
    weight: 20,
    status: '正常'
  },
  {
    name: '安全运营效率',
    code: 'SEC_OP_EFF',
    description: '安全运营工作的效率评分',
    unit: '分',
    weight: 20,
    status: '正常'
  }
])

const timeRange = ref('7')

const analysis = ref([
  {
    title: '平均响应时间',
    value: '15分钟',
    trend: -20
  },
  {
    title: '漏洞修复率',
    value: '85%',
    trend: 5
  },
  {
    title: '基线符合率',
    value: '92%',
    trend: 2
  },
  {
    title: '事件处理率',
    value: '95%',
    trend: 3
  },
  {
    title: '运营效率',
    value: '88分',
    trend: 8
  },
  {
    title: '安全评分',
    value: '92分',
    trend: 5
  }
])

const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const form = ref({
  name: '',
  code: '',
  description: '',
  unit: '',
  weight: 0
})

const getStatusType = (status: string): string => {
  switch (status) {
    case '正常':
      return 'success'
    case '异常':
      return 'danger'
    default:
      return 'info'
  }
}

const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    name: '',
    code: '',
    description: '',
    unit: '',
    weight: 0
  }
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm('确认删除该指标吗？', '提示', {
    type: 'warning'
  }).then(() => {
    const index = metrics.value.findIndex(item => item.code === row.code)
    if (index > -1) {
      metrics.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  })
}

const handleSubmit = () => {
  if (dialogType.value === 'add') {
    metrics.value.push({
      ...form.value,
      status: '正常'
    })
    ElMessage.success('添加成功')
  } else {
    const index = metrics.value.findIndex(item => item.code === form.value.code)
    if (index > -1) {
      metrics.value[index] = {
        ...form.value,
        status: '正常'
      }
      ElMessage.success('更新成功')
    }
  }
  dialogVisible.value = false
}

const handleSave = () => {
  ElMessage.success('保存成功')
}

onMounted(() => {
  // 初始化响应时间趋势图
  const responseTimeChart = echarts.init(responseTimeChartRef.value!)
  responseTimeChart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['2-14', '2-15', '2-16', '2-17', '2-18', '2-19', '2-20']
    },
    yAxis: {
      type: 'value',
      name: '分钟'
    },
    series: [
      {
        name: '响应时间',
        type: 'line',
        data: [20, 18, 15, 16, 14, 13, 12],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })

  // 初始化修复率趋势图
  const fixRateChart = echarts.init(fixRateChartRef.value!)
  fixRateChart.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['2-14', '2-15', '2-16', '2-17', '2-18', '2-19', '2-20']
    },
    yAxis: {
      type: 'value',
      name: '%',
      min: 0,
      max: 100
    },
    series: [
      {
        name: '修复率',
        type: 'line',
        data: [75, 78, 80, 82, 83, 84, 85],
        smooth: true,
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  })
})
</script>

<style scoped>
.metrics {
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

.metrics-trend {
  margin-top: 40px;
}

.metrics-analysis {
  margin-top: 40px;
}

.chart-container {
  height: 300px;
}

.analysis-content {
  text-align: center;
}

.analysis-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.analysis-compare {
  font-size: 14px;
  color: #909399;
}

.up {
  color: #67c23a;
}

.down {
  color: #f56c6c;
}
</style> 