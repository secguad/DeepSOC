<template>
  <div class="roles">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>角色权限</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAdd">新增角色</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleImport">批量导入</el-button>
          </div>
        </div>
      </template>

      <!-- 角色概览 -->
      <div class="role-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">角色总数</div>
                <div class="overview-value">8</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    2
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">系统角色</div>
                <div class="overview-value">3</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    1
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">自定义角色</div>
                <div class="overview-value">5</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    1
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">权限项</div>
                <div class="overview-value">32</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    4
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 角色列表 -->
      <div class="role-list">
        <div class="section-title">角色列表</div>
        <el-table :data="roleList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="name" label="角色名称" />
          <el-table-column prop="code" label="角色编码" />
          <el-table-column prop="type" label="角色类型" width="120">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="userCount" label="用户数" width="100" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleEdit(scope.row)">
                编辑
              </el-button>
              <el-button type="success" link @click="handlePermission(scope.row)">
                权限配置
              </el-button>
              <el-button type="warning" link @click="handleUser(scope.row)">
                用户管理
              </el-button>
              <el-button type="danger" link @click="handleDelete(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 角色表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增角色' : '编辑角色'"
      width="600px"
    >
      <el-form
        ref="roleFormRef"
        :model="roleForm"
        :rules="roleRules"
        label-width="100px"
      >
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色编码" prop="code">
          <el-input v-model="roleForm.code" placeholder="请输入角色编码" />
        </el-form-item>
        <el-form-item label="角色类型" prop="type">
          <el-select v-model="roleForm.type" placeholder="请选择角色类型">
            <el-option label="系统角色" value="system" />
            <el-option label="自定义角色" value="custom" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="roleForm.description"
            type="textarea"
            placeholder="请输入角色描述"
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

    <!-- 权限配置对话框 -->
    <el-dialog
      v-model="permissionVisible"
      title="权限配置"
      width="800px"
    >
      <el-tree
        ref="permissionTreeRef"
        :data="permissionTree"
        show-checkbox
        node-key="id"
        :props="{
          label: 'name',
          children: 'children'
        }"
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="permissionVisible = false">取消</el-button>
          <el-button type="primary" @click="handlePermissionSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowUp } from '@element-plus/icons-vue'

// 角色列表数据
const roleList = ref([
  {
    id: 'ROLE-2024-001',
    name: '超级管理员',
    code: 'SUPER_ADMIN',
    type: '系统角色',
    description: '系统最高权限',
    userCount: 1,
    status: '正常'
  },
  {
    id: 'ROLE-2024-002',
    name: '安全管理员',
    code: 'SECURITY_ADMIN',
    type: '系统角色',
    description: '安全管理相关权限',
    userCount: 3,
    status: '正常'
  },
  {
    id: 'ROLE-2024-003',
    name: '审计员',
    code: 'AUDITOR',
    type: '自定义角色',
    description: '系统审计相关权限',
    userCount: 5,
    status: '正常'
  }
])

// 表单相关
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const roleFormRef = ref()
const roleForm = ref({
  name: '',
  code: '',
  type: '',
  description: ''
})

const roleRules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入角色编码', trigger: 'blur' },
    { pattern: /^[A-Z_]+$/, message: '只能包含大写字母和下划线', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择角色类型', trigger: 'change' }
  ]
}

// 权限树相关
const permissionVisible = ref(false)
const permissionTreeRef = ref()
const permissionTree = ref([
  {
    id: '1',
    name: '系统管理',
    children: [
      {
        id: '1-1',
        name: '用户管理',
        children: [
          { id: '1-1-1', name: '查看用户' },
          { id: '1-1-2', name: '新增用户' },
          { id: '1-1-3', name: '编辑用户' },
          { id: '1-1-4', name: '删除用户' }
        ]
      },
      {
        id: '1-2',
        name: '角色管理',
        children: [
          { id: '1-2-1', name: '查看角色' },
          { id: '1-2-2', name: '新增角色' },
          { id: '1-2-3', name: '编辑角色' },
          { id: '1-2-4', name: '删除角色' }
        ]
      }
    ]
  },
  {
    id: '2',
    name: '安全中心',
    children: [
      {
        id: '2-1',
        name: '数据安全',
        children: [
          { id: '2-1-1', name: '查看数据' },
          { id: '2-1-2', name: '数据脱敏' },
          { id: '2-1-3', name: '数据加密' }
        ]
      },
      {
        id: '2-2',
        name: '行为分析',
        children: [
          { id: '2-2-1', name: '查看分析' },
          { id: '2-2-2', name: '配置规则' },
          { id: '2-2-3', name: '导出报告' }
        ]
      }
    ]
  }
])

const getTypeTag = (type: string): string => {
  switch (type) {
    case '系统角色':
      return 'danger'
    case '自定义角色':
      return 'info'
    default:
      return ''
  }
}

const getStatusTag = (status: string): string => {
  switch (status) {
    case '正常':
      return 'success'
    case '禁用':
      return 'danger'
    default:
      return ''
  }
}

const handleAdd = () => {
  dialogType.value = 'add'
  roleForm.value = {
    name: '',
    code: '',
    type: '',
    description: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  roleForm.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    `确定要删除角色 ${row.name} 吗？`,
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

const handlePermission = (row: any) => {
  permissionVisible.value = true
}

const handleUser = (row: any) => {
  ElMessage.success(`开始管理角色 ${row.name} 的用户`)
}

const handleImport = () => {
  ElMessage.success('开始导入角色')
}

const handleSubmit = () => {
  roleFormRef.value?.validate((valid: boolean) => {
    if (valid) {
      ElMessage.success(dialogType.value === 'add' ? '添加成功' : '修改成功')
      dialogVisible.value = false
    }
  })
}

const handlePermissionSubmit = () => {
  const checkedKeys = permissionTreeRef.value?.getCheckedKeys()
  const halfCheckedKeys = permissionTreeRef.value?.getHalfCheckedKeys()
  ElMessage.success('权限配置成功')
  permissionVisible.value = false
}
</script>

<style scoped>
.roles {
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

.role-overview {
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

.role-list {
  margin-top: 40px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 