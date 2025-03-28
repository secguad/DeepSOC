<template>
  <div class="alerts">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>告警管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleBatchProcess">批量处理</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出告警</el-button>
          </div>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="关键词">
            <el-input v-model="searchForm.keyword" placeholder="请输入关键词" />
          </el-form-item>
          <el-form-item label="告警级别">
            <el-select v-model="searchForm.level" placeholder="请选择告警级别">
              <el-option label="全部" value="" />
              <el-option label="高" value="high" />
              <el-option label="中" value="medium" />
              <el-option label="低" value="low" />
            </el-select>
          </el-form-item>
          <el-form-item label="处理状态">
            <el-select v-model="searchForm.status" placeholder="请选择处理状态">
              <el-option label="全部" value="" />
              <el-option label="未处理" value="unprocessed" />
              <el-option label="处理中" value="processing" />
              <el-option label="已处理" value="processed" />
              <el-option label="已忽略" value="ignored" />
            </el-select>
          </el-form-item>
          <el-form-item label="时间范围">
            <el-date-picker
              v-model="searchForm.timeRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 告警列表 -->
      <el-table
        :data="alertList"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="120" />
        <el-table-column prop="keyword" label="关键词" width="150" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getTypeTag(scope.row.type)">
              {{ getTypeLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="level" label="告警级别" width="100">
          <template #default="scope">
            <el-tag :type="getLevelTag(scope.row.level)">
              {{ getLevelLabel(scope.row.level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="告警内容" show-overflow-tooltip />
        <el-table-column prop="source" label="来源" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTag(scope.row.status)">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="告警时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button type="primary" link @click="handleProcess(scope.row)">
              处理
            </el-button>
            <el-button type="info" link @click="handleDetail(scope.row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 处理对话框 -->
    <el-dialog
      v-model="processDialogVisible"
      title="处理告警"
      width="600px"
    >
      <el-form
        ref="processFormRef"
        :model="processForm"
        :rules="processRules"
        label-width="100px"
      >
        <el-form-item label="处理状态" prop="status">
          <el-select v-model="processForm.status" placeholder="请选择处理状态">
            <el-option label="处理中" value="processing" />
            <el-option label="已处理" value="processed" />
            <el-option label="已忽略" value="ignored" />
          </el-select>
        </el-form-item>
        <el-form-item label="处理说明" prop="comment">
          <el-input
            v-model="processForm.comment"
            type="textarea"
            :rows="4"
            placeholder="请输入处理说明"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="processDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleProcessSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="告警详情"
      width="800px"
    >
      <div v-if="currentAlert" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentAlert.id }}</el-descriptions-item>
          <el-descriptions-item label="关键词">{{ currentAlert.keyword }}</el-descriptions-item>
          <el-descriptions-item label="类型">
            <el-tag :type="getTypeTag(currentAlert.type)">
              {{ getTypeLabel(currentAlert.type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="告警级别">
            <el-tag :type="getLevelTag(currentAlert.level)">
              {{ getLevelLabel(currentAlert.level) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="来源">{{ currentAlert.source }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTag(currentAlert.status)">
              {{ getStatusLabel(currentAlert.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="告警时间">{{ currentAlert.createTime }}</el-descriptions-item>
          <el-descriptions-item label="处理时间">{{ currentAlert.processTime || '-' }}</el-descriptions-item>
          <el-descriptions-item label="告警内容" :span="2">{{ currentAlert.content }}</el-descriptions-item>
          <el-descriptions-item label="处理说明" :span="2">{{ currentAlert.comment || '-' }}</el-descriptions-item>
          <el-descriptions-item label="相关链接" :span="2">
            <el-link type="primary" :href="currentAlert.url" target="_blank">
              {{ currentAlert.url }}
            </el-link>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'

// 搜索表单
const searchForm = reactive({
  keyword: '',
  level: '',
  status: '',
  timeRange: []
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

// 选中的告警
const selectedAlerts = ref<any[]>([])

// 告警列表数据
const alertList = ref([
  {
    id: 'ALERT-2024-001',
    keyword: 'example.com',
    type: 'domain',
    level: 'high',
    content: '发现公司域名在暗网论坛被提及，可能存在信息泄露风险',
    source: '暗网论坛',
    status: 'unprocessed',
    createTime: '2024-02-20 10:00:00',
    processTime: null,
    comment: null,
    url: 'http://example.com/alert/001'
  },
  {
    id: 'ALERT-2024-002',
    keyword: '产品A',
    type: 'product',
    level: 'medium',
    content: '产品A的源代码在暗网被出售',
    source: '暗网市场',
    status: 'processing',
    createTime: '2024-02-19 15:30:00',
    processTime: '2024-02-19 16:00:00',
    comment: '正在调查源代码泄露情况',
    url: 'http://example.com/alert/002'
  }
])

// 处理对话框相关
const processDialogVisible = ref(false)
const processFormRef = ref<FormInstance>()
const currentAlert = ref<any>(null)

// 处理表单数据
const processForm = reactive({
  status: '',
  comment: ''
})

// 处理表单验证规则
const processRules = {
  status: [
    { required: true, message: '请选择处理状态', trigger: 'change' }
  ],
  comment: [
    { required: true, message: '请输入处理说明', trigger: 'blur' }
  ]
}

// 详情对话框
const detailDialogVisible = ref(false)

// 获取类型标签样式
const getTypeTag = (type: string): string => {
  switch (type) {
    case 'company':
      return 'success'
    case 'product':
      return 'warning'
    case 'domain':
      return 'info'
    case 'ip':
      return 'danger'
    default:
      return ''
  }
}

// 获取类型显示文本
const getTypeLabel = (type: string): string => {
  switch (type) {
    case 'company':
      return '公司名称'
    case 'product':
      return '产品名称'
    case 'domain':
      return '域名'
    case 'ip':
      return 'IP地址'
    default:
      return ''
  }
}

// 获取告警级别标签样式
const getLevelTag = (level: string): string => {
  switch (level) {
    case 'high':
      return 'danger'
    case 'medium':
      return 'warning'
    case 'low':
      return 'info'
    default:
      return ''
  }
}

// 获取告警级别显示文本
const getLevelLabel = (level: string): string => {
  switch (level) {
    case 'high':
      return '高'
    case 'medium':
      return '中'
    case 'low':
      return '低'
    default:
      return ''
  }
}

// 获取状态标签样式
const getStatusTag = (status: string): string => {
  switch (status) {
    case 'unprocessed':
      return 'danger'
    case 'processing':
      return 'warning'
    case 'processed':
      return 'success'
    case 'ignored':
      return 'info'
    default:
      return ''
  }
}

// 获取状态显示文本
const getStatusLabel = (status: string): string => {
  switch (status) {
    case 'unprocessed':
      return '未处理'
    case 'processing':
      return '处理中'
    case 'processed':
      return '已处理'
    case 'ignored':
      return '已忽略'
    default:
      return ''
  }
}

// 搜索
const handleSearch = () => {
  // TODO: 实现搜索逻辑
  ElMessage.success('搜索成功')
}

// 重置搜索
const handleReset = () => {
  searchForm.keyword = ''
  searchForm.level = ''
  searchForm.status = ''
  searchForm.timeRange = []
  handleSearch()
}

// 选择变更
const handleSelectionChange = (selection: any[]) => {
  selectedAlerts.value = selection
}

// 批量处理
const handleBatchProcess = () => {
  if (selectedAlerts.value.length === 0) {
    ElMessage.warning('请选择要处理的告警')
    return
  }
  processDialogVisible.value = true
}

// 导出告警
const handleExport = () => {
  ElMessage.success('开始导出告警')
}

// 处理告警
const handleProcess = (row: any) => {
  currentAlert.value = row
  processForm.status = row.status
  processForm.comment = row.comment || ''
  processDialogVisible.value = true
}

// 提交处理
const handleProcessSubmit = async () => {
  if (!processFormRef.value) return
  
  await processFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现处理逻辑
      ElMessage.success('处理成功')
      processDialogVisible.value = false
    }
  })
}

// 查看详情
const handleDetail = (row: any) => {
  currentAlert.value = row
  detailDialogVisible.value = true
}

// 分页大小变更
const handleSizeChange = (val: number) => {
  pageSize.value = val
  handleSearch()
}

// 当前页变更
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  handleSearch()
}
</script>

<style scoped>
.alerts {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  margin-bottom: 20px;
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