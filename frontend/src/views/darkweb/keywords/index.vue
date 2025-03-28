<template>
  <div class="keywords">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>关键词管理</span>
          <el-button type="primary" @click="handleAdd">新增关键词</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="关键词">
            <el-input v-model="searchForm.keyword" placeholder="请输入关键词" />
          </el-form-item>
          <el-form-item label="类型">
            <el-select v-model="searchForm.type" placeholder="请选择类型">
              <el-option label="全部" value="" />
              <el-option label="公司名称" value="company" />
              <el-option label="产品名称" value="product" />
              <el-option label="域名" value="domain" />
              <el-option label="IP地址" value="ip" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态">
              <el-option label="全部" value="" />
              <el-option label="启用" value="enabled" />
              <el-option label="禁用" value="disabled" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 关键词列表 -->
      <el-table :data="keywordList" style="width: 100%">
        <el-table-column prop="id" label="ID" width="120" />
        <el-table-column prop="keyword" label="关键词" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getTypeTag(scope.row.type)">
              {{ getTypeLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="matchCount" label="匹配次数" width="120" />
        <el-table-column prop="lastMatchTime" label="最后匹配时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="'enabled'"
              :inactive-value="'disabled'"
              @change="handleStatusChange(scope.row)"
            />
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

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增关键词' : '编辑关键词'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="关键词" prop="keyword">
          <el-input v-model="form.keyword" placeholder="请输入关键词" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择类型">
            <el-option label="公司名称" value="company" />
            <el-option label="产品名称" value="product" />
            <el-option label="域名" value="domain" />
            <el-option label="IP地址" value="ip" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入描述"
          />
        </el-form-item>
        <el-form-item label="匹配规则" prop="rules">
          <el-checkbox-group v-model="form.rules">
            <el-checkbox label="exact">精确匹配</el-checkbox>
            <el-checkbox label="fuzzy">模糊匹配</el-checkbox>
            <el-checkbox label="regex">正则匹配</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="告警级别" prop="alertLevel">
          <el-select v-model="form.alertLevel" placeholder="请选择告警级别">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
          </el-select>
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
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'

// 搜索表单
const searchForm = reactive({
  keyword: '',
  type: '',
  status: ''
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

// 关键词列表数据
const keywordList = ref([
  {
    id: 'KEY-2024-001',
    keyword: 'example.com',
    type: 'domain',
    description: '公司主域名',
    matchCount: 156,
    lastMatchTime: '2024-02-20 10:00:00',
    status: 'enabled'
  },
  {
    id: 'KEY-2024-002',
    keyword: '产品A',
    type: 'product',
    description: '核心产品名称',
    matchCount: 89,
    lastMatchTime: '2024-02-19 15:30:00',
    status: 'enabled'
  }
])

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()

// 表单数据
const form = reactive({
  keyword: '',
  type: '',
  description: '',
  rules: ['exact'],
  alertLevel: 'medium'
})

// 表单验证规则
const rules = {
  keyword: [
    { required: true, message: '请输入关键词', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择类型', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入描述', trigger: 'blur' }
  ],
  alertLevel: [
    { required: true, message: '请选择告警级别', trigger: 'change' }
  ]
}

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

// 搜索
const handleSearch = () => {
  // TODO: 实现搜索逻辑
  ElMessage.success('搜索成功')
}

// 重置搜索
const handleReset = () => {
  searchForm.keyword = ''
  searchForm.type = ''
  searchForm.status = ''
  handleSearch()
}

// 新增关键词
const handleAdd = () => {
  dialogType.value = 'add'
  form.keyword = ''
  form.type = ''
  form.description = ''
  form.rules = ['exact']
  form.alertLevel = 'medium'
  dialogVisible.value = true
}

// 编辑关键词
const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 删除关键词
const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    '确定要删除该关键词吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 实现删除逻辑
    ElMessage.success('删除成功')
  })
}

// 状态变更
const handleStatusChange = (row: any) => {
  // TODO: 实现状态变更逻辑
  ElMessage.success('状态更新成功')
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现提交逻辑
      ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
      dialogVisible.value = false
    }
  })
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
.keywords {
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
</style> 