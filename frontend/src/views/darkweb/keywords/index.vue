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
            <el-input v-model="searchForm.word" placeholder="请输入关键词" />
          </el-form-item>
          <el-form-item label="类型">
            <el-select v-model="searchForm.category" placeholder="请选择类型">
              <el-option label="全部" value="" />
              <el-option label="公司名称" value="company" />
              <el-option label="产品名称" value="product" />
              <el-option label="域名" value="domain" />
              <el-option label="IP地址" value="ip" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.is_active" placeholder="请选择状态">
              <el-option label="全部" value="" />
              <el-option label="启用" value="true" />
              <el-option label="禁用" value="false" />
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
        <el-table-column prop="word" label="关键词" />
        <el-table-column prop="category" label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getTypeTag(scope.row.category)">
              {{ getTypeLabel(scope.row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="matchCount" label="匹配次数" width="120" />
        <el-table-column prop="lastMatchTime" label="最后匹配时间" width="180" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="scope">
            <el-switch
              v-model="scope.row.is_active"
              :active-value="true"
              :inactive-value="false"
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
        <el-form-item label="关键词" prop="word">
          <el-input v-model="form.word" placeholder="请输入关键词" />
        </el-form-item>
        <el-form-item label="类型" prop="category">
          <el-select v-model="form.category" placeholder="请选择类型">
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { getKeywords, createKeyword, updateKeyword, deleteKeyword } from '@/api/keyword'

// 搜索表单
const searchForm = reactive({
  word: '',
  category: '',
  is_active: ''
})

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 关键词列表数据
const keywordList = ref([])

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()

// 表单数据
const form = reactive({
  id: undefined as number | undefined,
  word: '',
  category: '',
  description: '',
  is_active: true
})

// 表单验证规则
const rules = {
  word: [
    { required: true, message: '请输入关键词', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择类型', trigger: 'change' }
  ]
}

// 获取关键词列表
const fetchKeywords = async () => {
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      word: searchForm.word,
      category: searchForm.category,
      is_active: searchForm.is_active
    }
    const res = await getKeywords(params)
    if (res.code === 0) {
      keywordList.value = res.data.items
      total.value = res.data.total
    }
  } catch (error) {
    console.error('获取关键词列表失败:', error)
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchKeywords()
}

// 重置
const handleReset = () => {
  searchForm.word = ''
  searchForm.category = ''
  searchForm.is_active = ''
  handleSearch()
}

// 新增关键词
const handleAdd = () => {
  dialogType.value = 'add'
  form.id = undefined
  form.word = ''
  form.category = ''
  form.description = ''
  form.is_active = true
  dialogVisible.value = true
}

// 编辑关键词
const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  form.id = row.id
  form.word = row.word
  form.category = row.category
  form.description = row.description
  form.is_active = row.is_active
  dialogVisible.value = true
}

// 删除关键词
const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确认删除该关键词吗？', '提示', {
      type: 'warning'
    })
    const res = await deleteKeyword(row.id)
    if (res.code === 0) {
      ElMessage.success('删除成功')
      fetchKeywords()
    }
  } catch (error) {
    console.error('删除关键词失败:', error)
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          const res = await createKeyword(form)
          if (res.code === 0) {
            ElMessage.success('添加成功')
            dialogVisible.value = false
            fetchKeywords()
          }
        } else {
          const res = await updateKeyword(form.id!, form)
          if (res.code === 0) {
            ElMessage.success('更新成功')
            dialogVisible.value = false
            fetchKeywords()
          }
        }
      } catch (error) {
        console.error('提交表单失败:', error)
      }
    }
  })
}

// 状态切换
const handleStatusChange = async (row: any) => {
  try {
    const res = await updateKeyword(row.id, { is_active: row.is_active })
    if (res.code === 0) {
      ElMessage.success('状态更新成功')
    }
  } catch (error) {
    console.error('更新状态失败:', error)
    row.is_active = !row.is_active // 恢复状态
  }
}

// 分页大小改变
const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchKeywords()
}

// 页码改变
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchKeywords()
}

// 获取类型标签样式
const getTypeTag = (type: string) => {
  const map: Record<string, string> = {
    company: 'success',
    product: 'warning',
    domain: 'info',
    ip: 'danger'
  }
  return map[type] || 'info'
}

// 获取类型标签文本
const getTypeLabel = (type: string) => {
  const map: Record<string, string> = {
    company: '公司名称',
    product: '产品名称',
    domain: '域名',
    ip: 'IP地址'
  }
  return map[type] || type
}

// 页面加载时获取数据
onMounted(() => {
  fetchKeywords()
})
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