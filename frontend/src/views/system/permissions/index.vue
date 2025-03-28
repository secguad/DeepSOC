<template>
  <div class="permissions">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>权限管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAdd">新增权限</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleImport">批量导入</el-button>
          </div>
        </div>
      </template>

      <!-- 权限概览 -->
      <div class="permission-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">总权限数</div>
                <div class="overview-value">128</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    12
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">菜单权限</div>
                <div class="overview-value">45</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    5
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">操作权限</div>
                <div class="overview-value">83</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    7
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">数据权限</div>
                <div class="overview-value">32</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    3
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 权限列表 -->
      <div class="permission-list">
        <div class="section-title">权限列表</div>
        <el-table :data="permissionList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="name" label="权限名称" width="150" />
          <el-table-column prop="code" label="权限编码" width="150" />
          <el-table-column prop="type" label="类型" width="100">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="parent" label="上级权限" width="150" />
          <el-table-column prop="path" label="路径" />
          <el-table-column prop="description" label="描述" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleEdit(scope.row)">
                编辑
              </el-button>
              <el-button type="success" link @click="handleAssign(scope.row)">
                分配
              </el-button>
              <el-button type="danger" link @click="handleDelete(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 权限表单对话框 -->
    <el-dialog
      v-model="formVisible"
      :title="formType === 'add' ? '新增权限' : '编辑权限'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="permissionForm"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="permissionForm.name" placeholder="请输入权限名称" />
        </el-form-item>
        <el-form-item label="权限编码" prop="code">
          <el-input v-model="permissionForm.code" placeholder="请输入权限编码" />
        </el-form-item>
        <el-form-item label="权限类型" prop="type">
          <el-select v-model="permissionForm.type" placeholder="请选择权限类型">
            <el-option label="菜单权限" value="menu" />
            <el-option label="操作权限" value="operation" />
            <el-option label="数据权限" value="data" />
          </el-select>
        </el-form-item>
        <el-form-item label="上级权限" prop="parent">
          <el-select v-model="permissionForm.parent" placeholder="请选择上级权限">
            <el-option label="无" value="" />
            <el-option
              v-for="item in parentOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="路径" prop="path">
          <el-input v-model="permissionForm.path" placeholder="请输入路径" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="permissionForm.description"
            type="textarea"
            placeholder="请输入描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="formVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 权限分配对话框 -->
    <el-dialog
      v-model="assignVisible"
      title="权限分配"
      width="800px"
    >
      <div v-if="currentItem" class="assign-content">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="角色分配" name="roles">
            <el-table
              :data="roleList"
              style="width: 100%"
              @selection-change="handleRoleSelectionChange"
            >
              <el-table-column type="selection" width="55" />
              <el-table-column prop="id" label="ID" width="120" />
              <el-table-column prop="name" label="角色名称" width="150" />
              <el-table-column prop="code" label="角色编码" width="150" />
              <el-table-column prop="description" label="描述" />
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="用户分配" name="users">
            <el-table
              :data="userList"
              style="width: 100%"
              @selection-change="handleUserSelectionChange"
            >
              <el-table-column type="selection" width="55" />
              <el-table-column prop="id" label="ID" width="120" />
              <el-table-column prop="username" label="用户名" width="150" />
              <el-table-column prop="name" label="姓名" width="150" />
              <el-table-column prop="department" label="部门" width="150" />
              <el-table-column prop="email" label="邮箱" />
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="assignVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAssignSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowUp } from '@element-plus/icons-vue'

// 权限列表数据
const permissionList = ref([
  {
    id: 'PERM-2024-001',
    name: '系统管理',
    code: 'system:manage',
    type: '菜单权限',
    parent: '',
    path: '/system',
    description: '系统管理模块'
  },
  {
    id: 'PERM-2024-002',
    name: '用户管理',
    code: 'system:user:manage',
    type: '菜单权限',
    parent: 'PERM-2024-001',
    path: '/system/users',
    description: '用户管理模块'
  }
])

// 表单相关
const formVisible = ref(false)
const formType = ref<'add' | 'edit'>('add')
const formRef = ref()
const permissionForm = ref({
  name: '',
  code: '',
  type: '',
  parent: '',
  path: '',
  description: ''
})

const formRules = {
  name: [{ required: true, message: '请输入权限名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入权限编码', trigger: 'blur' }],
  type: [{ required: true, message: '请选择权限类型', trigger: 'change' }]
}

// 上级权限选项
const parentOptions = ref([
  {
    id: 'PERM-2024-001',
    name: '系统管理'
  }
])

// 分配相关
const assignVisible = ref(false)
const currentItem = ref<any>(null)
const activeTab = ref('roles')
const roleList = ref([
  {
    id: 'ROLE-2024-001',
    name: '系统管理员',
    code: 'admin',
    description: '系统管理员角色'
  }
])
const userList = ref([
  {
    id: 'USER-2024-001',
    username: 'admin',
    name: '管理员',
    department: '技术部',
    email: 'admin@example.com'
  }
])

const getTypeTag = (type: string): string => {
  switch (type) {
    case '菜单权限':
      return 'primary'
    case '操作权限':
      return 'success'
    case '数据权限':
      return 'warning'
    default:
      return ''
  }
}

const handleAdd = () => {
  formType.value = 'add'
  permissionForm.value = {
    name: '',
    code: '',
    type: '',
    parent: '',
    path: '',
    description: ''
  }
  formVisible.value = true
}

const handleEdit = (row: any) => {
  formType.value = 'edit'
  permissionForm.value = { ...row }
  formVisible.value = true
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    '确定要删除该权限吗？此操作不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('删除成功')
  })
}

const handleSubmit = () => {
  formRef.value?.validate((valid: boolean) => {
    if (valid) {
      ElMessage.success(formType.value === 'add' ? '添加成功' : '修改成功')
      formVisible.value = false
    }
  })
}

const handleImport = () => {
  ElMessage.success('开始导入权限')
}

const handleAssign = (row: any) => {
  currentItem.value = row
  assignVisible.value = true
}

const handleRoleSelectionChange = (selection: any[]) => {
  console.log('选中的角色：', selection)
}

const handleUserSelectionChange = (selection: any[]) => {
  console.log('选中的用户：', selection)
}

const handleAssignSubmit = () => {
  ElMessage.success('权限分配成功')
  assignVisible.value = false
}
</script>

<style scoped>
.permissions {
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

.permission-overview {
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

.permission-list {
  margin-top: 20px;
}

.assign-content {
  padding: 20px;
}
</style> 