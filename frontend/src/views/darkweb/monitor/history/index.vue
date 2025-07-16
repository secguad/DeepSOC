<template>
  <div class="history-monitor-container">
    <el-card class="config-card">
      <template #header>
        <div class="card-header">
          <span>扫描配置</span>
          <el-button type="primary" @click="handleStartScan">开始扫描</el-button>
        </div>
      </template>
      <el-form :model="scanConfig" label-width="120px">
        <el-form-item label="扫描范围">
          <el-date-picker
            v-model="scanConfig.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :shortcuts="dateShortcuts"
          />
        </el-form-item>
        <el-form-item label="扫描间隔">
          <el-input-number
            v-model="scanConfig.interval"
            :min="1"
            :max="24"
            placeholder="请输入扫描间隔（小时）"
          />
          <span class="unit-text">小时</span>
        </el-form-item>
        <el-form-item label="扫描深度">
          <el-slider
            v-model="scanConfig.depth"
            :min="1"
            :max="5"
            :marks="{
              1: '浅',
              3: '中',
              5: '深'
            }"
          />
          <span class="depth-text">{{ getDepthText(scanConfig.depth) }}</span>
        </el-form-item>
        <el-form-item label="扫描类型">
          <el-checkbox-group v-model="scanConfig.types">
            <el-checkbox label="forum">论坛</el-checkbox>
            <el-checkbox label="market">交易市场</el-checkbox>
            <el-checkbox label="paste">数据粘贴</el-checkbox>
            <el-checkbox label="github">GitHub</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="result-card">
      <template #header>
        <div class="card-header">
          <span>扫描结果</span>
          <div class="header-actions">
            <el-button type="success" @click="handleExport">导出结果</el-button>
            <el-button type="danger" @click="handleClear">清空结果</el-button>
          </div>
        </div>
      </template>
      <el-table :data="scanResults" style="width: 100%">
        <el-table-column prop="time" label="发现时间" width="180" />
        <el-table-column prop="source" label="数据来源" width="120" />
        <el-table-column prop="type" label="泄露类型" width="120" />
        <el-table-column prop="content" label="泄露内容" />
        <el-table-column prop="reliability" label="可信度" width="100">
          <template #default="scope">
            <el-tag :type="getReliabilityType(scope.row.reliability)">
              {{ scope.row.reliability }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" link @click="handleViewDetail(scope.row)">
              查看详情
            </el-button>
            <el-button type="danger" link @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
        />
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="泄露详情"
      width="60%"
    >
      <div v-if="currentDetail" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="发现时间">{{ currentDetail.time }}</el-descriptions-item>
          <el-descriptions-item label="数据来源">{{ currentDetail.source }}</el-descriptions-item>
          <el-descriptions-item label="泄露类型">{{ currentDetail.type }}</el-descriptions-item>
          <el-descriptions-item label="可信度">
            <el-tag :type="getReliabilityType(currentDetail.reliability)">
              {{ currentDetail.reliability }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="泄露内容" :span="2">
            {{ currentDetail.content }}
          </el-descriptions-item>
          <el-descriptions-item label="原始链接" :span="2">
            <el-link type="primary" :href="currentDetail.url" target="_blank">
              {{ currentDetail.url }}
            </el-link>
          </el-descriptions-item>
          <el-descriptions-item label="相关截图" :span="2">
            <el-image
              v-if="currentDetail.screenshot"
              :src="currentDetail.screenshot"
              :preview-src-list="[currentDetail.screenshot]"
            />
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 扫描配置
const scanConfig = reactive({
  dateRange: [],
  interval: 24,
  depth: 3,
  types: ['forum', 'market']
})

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  },
  {
    text: '最近三月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    }
  }
]

// 获取扫描深度文本
const getDepthText = (depth: number) => {
  switch (depth) {
    case 1:
      return '浅层扫描（仅扫描表层数据）'
    case 3:
      return '中层扫描（扫描表层和部分深层数据）'
    case 5:
      return '深层扫描（全面扫描所有数据）'
    default:
      return ''
  }
}

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

// 扫描结果
const scanResults = ref([
  {
    time: '2024-03-29 10:30:00',
    source: '暗网论坛',
    type: '账号泄露',
    content: '发现公司邮箱账号在暗网论坛泄露',
    reliability: '高',
    url: 'http://example.com/leak1',
    screenshot: 'http://example.com/screenshot1.jpg'
  },
  {
    time: '2024-03-29 10:25:00',
    source: '交易市场',
    type: '文档泄露',
    content: '发现内部文档在暗网交易平台出现',
    reliability: '中',
    url: 'http://example.com/leak2',
    screenshot: 'http://example.com/screenshot2.jpg'
  }
])

// 详情对话框
const detailVisible = ref(false)
const currentDetail = ref(null)

// 获取可信度对应的标签类型
const getReliabilityType = (reliability: string) => {
  switch (reliability) {
    case '高':
      return 'danger'
    case '中':
      return 'warning'
    case '低':
      return 'info'
    default:
      return 'info'
  }
}

// 开始扫描
const handleStartScan = () => {
  if (!scanConfig.dateRange || scanConfig.dateRange.length !== 2) {
    ElMessage.warning('请选择扫描范围')
    return
  }
  if (scanConfig.types.length === 0) {
    ElMessage.warning('请至少选择一种扫描类型')
    return
  }
  ElMessage.success('开始扫描')
  // TODO: 调用后端API开始扫描
}

// 导出结果
const handleExport = () => {
  ElMessage.success('导出成功')
  // TODO: 调用后端API导出结果
}

// 清空结果
const handleClear = () => {
  ElMessageBox.confirm('确定要清空所有扫描结果吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    scanResults.value = []
    ElMessage.success('清空成功')
  })
}

// 查看详情
const handleViewDetail = (row: any) => {
  currentDetail.value = row
  detailVisible.value = true
}

// 删除结果
const handleDelete = (row: any) => {
  ElMessageBox.confirm('确定要删除这条记录吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    const index = scanResults.value.findIndex(item => item === row)
    if (index > -1) {
      scanResults.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  })
}
</script>

<style scoped>
.history-monitor-container {
  padding: 20px;
}

.config-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.unit-text {
  margin-left: 8px;
  color: #606266;
}

.depth-text {
  margin-left: 16px;
  color: #606266;
}

.result-card {
  margin-top: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.detail-content {
  padding: 20px;
}
</style> 