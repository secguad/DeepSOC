<template>
  <div class="realtime-monitor-container">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="monitor-card">
          <template #header>
            <div class="card-header">
              <span>实时监控</span>
              <div class="header-actions">
                <el-button type="primary" @click="handleStartMonitor" :disabled="isMonitoring">
                  开始监控
                </el-button>
                <el-button type="danger" @click="handleStopMonitor" :disabled="!isMonitoring">
                  停止监控
                </el-button>
              </div>
            </div>
          </template>
          <div class="monitor-content">
            <div class="status-bar">
              <el-tag :type="isMonitoring ? 'success' : 'info'">
                {{ isMonitoring ? '监控中' : '已停止' }}
              </el-tag>
              <span class="monitor-time" v-if="isMonitoring">
                已运行: {{ formatDuration(runTime) }}
              </span>
            </div>
            <div class="message-list" ref="messageList">
              <div
                v-for="(message, index) in messages"
                :key="index"
                class="message-item"
                :class="{ 'new': message.isNew }"
              >
                <div class="message-time">{{ message.time }}</div>
                <div class="message-content">
                  <div class="message-header">
                    <el-tag size="small" :type="getSourceType(message.source)">
                      {{ message.source }}
                    </el-tag>
                    <el-tag size="small" :type="getReliabilityType(message.reliability)">
                      {{ message.reliability }}
                    </el-tag>
                  </div>
                  <div class="message-body">{{ message.content }}</div>
                  <div class="message-footer">
                    <el-button type="primary" link @click="handleViewDetail(message)">
                      查看详情
                    </el-button>
                    <el-button type="danger" link @click="handleIgnore(message)">
                      忽略
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stats-card">
          <template #header>
            <div class="card-header">
              <span>监控统计</span>
            </div>
          </template>
          <div class="stats-content">
            <div class="stat-item">
              <div class="stat-label">今日消息数</div>
              <div class="stat-value">{{ todayCount }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">高可信度</div>
              <div class="stat-value high">{{ highReliabilityCount }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">中可信度</div>
              <div class="stat-value medium">{{ mediumReliabilityCount }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">低可信度</div>
              <div class="stat-value low">{{ lowReliabilityCount }}</div>
            </div>
          </div>
        </el-card>

        <el-card class="channels-card">
          <template #header>
            <div class="card-header">
              <span>监控频道</span>
              <el-button type="primary" link @click="handleManageChannels">
                管理频道
              </el-button>
            </div>
          </template>
          <div class="channels-content">
            <el-table :data="monitorChannels" style="width: 100%">
              <el-table-column prop="name" label="频道名称" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
                    {{ scope.row.status === 'active' ? '活跃' : '未活跃' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="lastUpdate" label="最后更新" width="160" />
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="消息详情"
      width="60%"
    >
      <div v-if="currentDetail" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="时间">{{ currentDetail.time }}</el-descriptions-item>
          <el-descriptions-item label="来源">
            <el-tag :type="getSourceType(currentDetail.source)">
              {{ currentDetail.source }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="可信度">
            <el-tag :type="getReliabilityType(currentDetail.reliability)">
              {{ currentDetail.reliability }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="内容" :span="2">
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

    <!-- 频道管理对话框 -->
    <el-dialog
      v-model="channelsVisible"
      title="频道管理"
      width="50%"
    >
      <el-table :data="allChannels" style="width: 100%">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="频道名称" />
        <el-table-column prop="type" label="类型" />
        <el-table-column prop="description" label="描述" />
      </el-table>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="channelsVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveChannels">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'

// 监控状态
const isMonitoring = ref(false)
const runTime = ref(0)
let timer: number | null = null

// 消息列表
const messages = ref([
  {
    time: '2024-03-29 10:30:00',
    source: '暗网论坛',
    content: '发现公司邮箱账号在暗网论坛泄露',
    reliability: '高',
    isNew: true,
    url: 'http://example.com/leak1',
    screenshot: 'http://example.com/screenshot1.jpg'
  },
  {
    time: '2024-03-29 10:25:00',
    source: '交易市场',
    content: '发现内部文档在暗网交易平台出现',
    reliability: '中',
    isNew: false,
    url: 'http://example.com/leak2',
    screenshot: 'http://example.com/screenshot2.jpg'
  }
])

// 统计信息
const todayCount = ref(12)
const highReliabilityCount = ref(5)
const mediumReliabilityCount = ref(4)
const lowReliabilityCount = ref(3)

// 监控频道
const monitorChannels = ref([
  {
    name: '暗网论坛1',
    status: 'active',
    lastUpdate: '2024-03-29 10:30:00'
  },
  {
    name: '交易市场1',
    status: 'active',
    lastUpdate: '2024-03-29 10:25:00'
  },
  {
    name: '数据粘贴1',
    status: 'inactive',
    lastUpdate: '2024-03-29 09:00:00'
  }
])

// 所有可用频道
const allChannels = ref([
  {
    name: '暗网论坛1',
    type: '论坛',
    description: '主要暗网论坛'
  },
  {
    name: '交易市场1',
    type: '市场',
    description: '数据交易市场'
  },
  {
    name: '数据粘贴1',
    type: '粘贴',
    description: '数据粘贴网站'
  },
  {
    name: 'GitHub',
    type: '代码',
    description: 'GitHub代码仓库'
  }
])

// 详情对话框
const detailVisible = ref(false)
const currentDetail = ref(null)

// 频道管理对话框
const channelsVisible = ref(false)

// 获取来源对应的标签类型
const getSourceType = (source: string) => {
  switch (source) {
    case '暗网论坛':
      return 'danger'
    case '交易市场':
      return 'warning'
    case '数据粘贴':
      return 'info'
    default:
      return 'info'
  }
}

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

// 格式化运行时间
const formatDuration = (seconds: number) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const remainingSeconds = seconds % 60
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 开始监控
const handleStartMonitor = () => {
  isMonitoring.value = true
  runTime.value = 0
  timer = window.setInterval(() => {
    runTime.value++
  }, 1000)
  ElMessage.success('开始监控')
  // TODO: 调用后端API开始监控
}

// 停止监控
const handleStopMonitor = () => {
  isMonitoring.value = false
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  ElMessage.success('停止监控')
  // TODO: 调用后端API停止监控
}

// 查看详情
const handleViewDetail = (message: any) => {
  currentDetail.value = message
  detailVisible.value = true
}

// 忽略消息
const handleIgnore = (message: any) => {
  const index = messages.value.findIndex(item => item === message)
  if (index > -1) {
    messages.value.splice(index, 1)
    ElMessage.success('已忽略该消息')
  }
}

// 管理频道
const handleManageChannels = () => {
  channelsVisible.value = true
}

// 保存频道设置
const handleSaveChannels = () => {
  channelsVisible.value = false
  ElMessage.success('保存成功')
  // TODO: 调用后端API保存频道设置
}

// 组件卸载时清理定时器
onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.realtime-monitor-container {
  padding: 20px;
}

.monitor-card {
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

.monitor-content {
  height: calc(100vh - 300px);
  display: flex;
  flex-direction: column;
}

.status-bar {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.monitor-time {
  color: #606266;
  font-size: 14px;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 10px;
}

.message-item {
  margin-bottom: 20px;
  padding: 15px;
  border-radius: 4px;
  background-color: #f8f9fa;
  transition: all 0.3s;
}

.message-item.new {
  background-color: #f0f9ff;
  border-left: 4px solid #409EFF;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
}

.message-header {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
}

.message-body {
  color: #303133;
  margin-bottom: 8px;
  line-height: 1.5;
}

.message-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.stats-card,
.channels-card {
  margin-bottom: 20px;
}

.stats-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.stat-label {
  color: #606266;
  font-size: 14px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-value.high {
  color: #F56C6C;
}

.stat-value.medium {
  color: #E6A23C;
}

.stat-value.low {
  color: #909399;
}

.detail-content {
  padding: 20px;
}
</style> 