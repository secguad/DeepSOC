<template>
  <div class="users">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAdd">新增用户</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleImport">批量导入</el-button>
          </div>
        </div>
      </template>

      <!-- 用户概览 -->
      <div class="user-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">总用户数</div>
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
                <div class="overview-title">活跃用户</div>
                <div class="overview-value">98</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    8
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">管理员</div>
                <div class="overview-value">12</div>
                <div class="overview-trend">
                  较上月
                  <span class="down">
                    2
                    <el-icon><ArrowDown /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">普通用户</div>
                <div class="overview-value">116</div>
                <div class="overview-trend">
                  较上月
                  <span class="up">
                    14
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 用户列表 -->
      <div class="user-list">
        <div class="section-title">用户列表</div>
        <el-table :data="userList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="role" label="角色" width="120">
            <template #default="scope">
              <el-tag :type="getRoleTag(scope.row.role)">
                {{ scope.row.role }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="department" label="部门" width="150" />
          <el-table-column prop="email" label="邮箱" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusTag(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="lastLogin" label="最后登录" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleEdit(scope.row)">
                编辑
              </el-button>
              <el-button type="success" link @click="handleReset(scope.row)">
                重置密码
              </el-button>
              <el-button type="danger" link @click="handleDelete(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 用户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增用户' : '编辑用户'"
      width="600px"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="userForm.department" placeholder="请输入部门" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogType === 'add'">
          <el-input
            v-model="userForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
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
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

// 用户列表数据
const userList = ref([
  {
    id: 'USER-2024-001',
    username: 'admin',
    name: '管理员',
    role: '管理员',
    department: '系统管理部',
    email: 'admin@example.com',
    status: '正常',
    lastLogin: '2024-02-20 10:00:00'
  },
  {
    id: 'USER-2024-002',
    username: 'user1',
    name: '张三',
    role: '普通用户',
    department: '安全部',
    email: 'zhangsan@example.com',
    status: '正常',
    lastLogin: '2024-02-20 09:30:00'
  }
])

// 表单相关
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const userFormRef = ref()
const userForm = ref({
  username: '',
  name: '',
  role: '',
  department: '',
  email: '',
  password: ''
})

const userRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  department: [
    { required: true, message: '请输入部门', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ]
}

const getRoleTag = (role: string): string => {
  switch (role) {
    case '管理员':
      return 'danger'
    case '普通用户':
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
  userForm.value = {
    username: '',
    name: '',
    role: '',
    department: '',
    email: '',
    password: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  userForm.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    `确定要删除用户 ${row.name} 吗？`,
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

const handleReset = (row: any) => {
  ElMessageBox.confirm(
    `确定要重置用户 ${row.name} 的密码吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('密码重置成功')
  })
}

const handleImport = () => {
  ElMessage.success('开始导入用户')
}

const handleSubmit = () => {
  userFormRef.value?.validate((valid: boolean) => {
    if (valid) {
      ElMessage.success(dialogType.value === 'add' ? '添加成功' : '修改成功')
      dialogVisible.value = false
    }
  })
}
</script>

<style scoped>
.users {
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

.user-overview {
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

.user-list {
  margin-top: 40px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 