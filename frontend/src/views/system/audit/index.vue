<template>
  <div class="audit">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>操作审计</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleExport">导出审计日志</el-button>
            <el-button type="danger" style="margin-left: 16px" @click="handleClear">清理日志</el-button>
          </div>
        </div>
      </template>

      <!-- 审计概览 -->
      <div class="audit-overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">今日操作</div>
                <div class="overview-value">256</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    32
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">敏感操作</div>
                <div class="overview-value">12</div>
                <div class="overview-trend">
                  较昨日
                  <span class="down">
                    3
                    <el-icon><ArrowDown /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">异常操作</div>
                <div class="overview-value">5</div>
                <div class="overview-trend">
                  较昨日
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
                <div class="overview-title">操作类型</div>
                <div class="overview-value">8</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    1
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 搜索区域 -->
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="操作类型">
            <el-select v-model="searchForm.type" placeholder="请选择操作类型">
              <el-option label="全部" value="" />
              <el-option label="登录" value="login" />
              <el-option label="新增" value="create" />
              <el-option label="修改" value="update" />
              <el-option label="删除" value="delete" />
              <el-option label="导出" value="export" />
            </el-select>
          </el-form-item>
          <el-form-item label="操作人">
            <el-input v-model="searchForm.operator" placeholder="请输入操作人" />
          </el-form-item>
          <el-form-item label="IP地址">
            <el-input v-model="searchForm.ip" placeholder="请输入IP地址" />
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

      <!-- 审计日志列表 -->
      <div class="audit-list">
        <div class="section-title">审计日志</div>
        <el-table :data="auditList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="type" label="操作类型" width="100">
            <template #default="scope">
              <el-tag :type="getTypeTag(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="module" label="操作模块" width="120" />
          <el-table-column prop="operator" label="操作人" width="120" />
          <el-table-column prop="action" label="操作内容" />
          <el-table-column prop="ip" label="IP地址" width="140" />
          <el-table-column prop="time" label="操作时间" width="180" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === '成功' ? 'success' : 'danger'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 审计详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="审计详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="操作类型">
            <el-tag :type="getTypeTag(currentItem.type)">
              {{ currentItem.type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="操作模块">{{ currentItem.module }}</el-descriptions-item>
          <el-descriptions-item label="操作人">{{ currentItem.operator }}</el-descriptions-item>
          <el-descriptions-item label="IP地址">{{ currentItem.ip }}</el-descriptions-item>
          <el-descriptions-item label="操作时间">{{ currentItem.time }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentItem.status === '成功' ? 'success' : 'danger'">
              {{ currentItem.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="操作内容" :span="2">{{ currentItem.action }}</el-descriptions-item>
          <el-descriptions-item label="请求参数" :span="2">
            <pre>{{ currentItem.request }}</pre>
          </el-descriptions-item>
          <el-descriptions-item label="响应结果" :span="2">
            <pre>{{ currentItem.response }}</pre>
          </el-descriptions-item>
          <el-descriptions-item label="错误信息" :span="2" v-if="currentItem.error">
            <pre class="error">{{ currentItem.error }}</pre>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

// 搜索表单
const searchForm = ref({
  type: '',
  operator: '',
  ip: '',
  timeRange: []
})

// 审计日志列表数据
const auditList = ref([
  {
    id: 'AUDIT-2024-001',
    type: '登录',
    module: '系统管理',
    operator: 'admin',
    action: '用户登录系统',
    ip: '192.168.1.100',
    time: '2024-02-20 10:00:00',
    status: '成功',
    request: '{"username": "admin", "password": "******"}',
    response: '{"code": 200, "message": "登录成功"}'
  },
  {
    id: 'AUDIT-2024-002',
    type: '删除',
    module: '用户管理',
    operator: 'admin',
    action: '删除用户',
    ip: '192.168.1.100',
    time: '2024-02-20 09:55:00',
    status: '失败',
    request: '{"userId": "USER-2024-003"}',
    response: '{"code": 404, "message": "用户不存在"}',
    error: '用户不存在，无法删除'
  }
])

const detailVisible = ref(false)
const currentItem = ref<any>(null)

const getTypeTag = (type: string): string => {
  switch (type) {
    case '登录':
      return 'primary'
    case '新增':
      return 'success'
    case '修改':
      return 'warning'
    case '删除':
      return 'danger'
    case '导出':
      return 'info'
    default:
      return ''
  }
}

const handleSearch = () => {
  ElMessage.success('开始搜索审计日志')
}

const handleReset = () => {
  searchForm.value = {
    type: '',
    operator: '',
    ip: '',
    timeRange: []
  }
}

const handleExport = () => {
  ElMessage.success('开始导出审计日志')
}

const handleClear = () => {
  ElMessageBox.confirm(
    '确定要清理审计日志吗？此操作不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('审计日志清理成功')
  })
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}
</script>

<style scoped>
.audit {
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

.audit-overview {
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

.search-area {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.audit-list {
  margin-top: 20px;
}

.detail-content {
  padding: 20px;
}

.detail-content pre {
  margin: 0;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.detail-content pre.error {
  background-color: #fef0f0;
  color: #f56c6c;
}
</style> 