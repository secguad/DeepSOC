<template>
  <div class="ai-assistant">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>AI助手</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleNewChat">新建对话</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出记录</el-button>
          </div>
        </div>
      </template>

      <!-- 对话概览 -->
      <div class="chat-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">今日对话</div>
                <div class="overview-value">25</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    5
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">解决问题</div>
                <div class="overview-value">18</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    3
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">知识库</div>
                <div class="overview-value">156</div>
                <div class="overview-trend">
                  较昨日
                  <span class="up">
                    12
                    <el-icon><ArrowUp /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 对话区域 -->
      <div class="chat-area">
        <div class="chat-messages" ref="messagesRef">
          <div v-for="(message, index) in messages" :key="index" class="message-item">
            <div :class="['message-content', message.type === 'user' ? 'user-message' : 'ai-message']">
              <div class="message-avatar">
                <el-avatar :size="40" :src="message.type === 'user' ? userAvatar : aiAvatar" />
              </div>
              <div class="message-text">
                <div class="message-time">{{ message.time }}</div>
                <div class="message-body">{{ message.content }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="chat-input">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题..."
            @keyup.enter.ctrl="handleSend"
          />
          <div class="input-actions">
            <el-button type="primary" @click="handleSend">发送</el-button>
            <el-button @click="handleClear">清空</el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 知识库对话框 -->
    <el-dialog
      v-model="knowledgeVisible"
      title="知识库管理"
      width="800px"
    >
      <div class="knowledge-content">
        <el-table :data="knowledgeList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="120" />
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="category" label="分类" width="120">
            <template #default="scope">
              <el-tag :type="getCategoryTag(scope.row.category)">
                {{ scope.row.category }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="updateTime" label="更新时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleEdit(scope.row)">
                编辑
              </el-button>
              <el-button type="success" link @click="handleTrain(scope.row)">
                训练
              </el-button>
              <el-button type="danger" link @click="handleDelete(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowUp } from '@element-plus/icons-vue'

// 用户和AI头像
const userAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
const aiAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

// 消息列表
const messages = ref([
  {
    type: 'ai',
    content: '您好！我是AI助手，有什么可以帮您的吗？',
    time: '2024-02-20 10:00:00'
  }
])

// 输入消息
const inputMessage = ref('')

// 知识库列表
const knowledgeList = ref([
  {
    id: 'KB-2024-001',
    title: '系统使用指南',
    category: '文档',
    updateTime: '2024-02-20 10:00:00'
  },
  {
    id: 'KB-2024-002',
    title: '常见问题解答',
    category: 'FAQ',
    updateTime: '2024-02-20 09:30:00'
  }
])

const knowledgeVisible = ref(false)
const messagesRef = ref<HTMLElement | null>(null)

const getCategoryTag = (category: string): string => {
  switch (category) {
    case '文档':
      return 'primary'
    case 'FAQ':
      return 'success'
    case '教程':
      return 'warning'
    default:
      return 'info'
  }
}

const handleNewChat = () => {
  messages.value = [
    {
      type: 'ai',
      content: '您好！我是AI助手，有什么可以帮您的吗？',
      time: new Date().toLocaleString()
    }
  ]
}

const handleExport = () => {
  ElMessage.success('导出对话记录...')
}

const handleSend = async () => {
  if (!inputMessage.value.trim()) return

  // 添加用户消息
  messages.value.push({
    type: 'user',
    content: inputMessage.value,
    time: new Date().toLocaleString()
  })

  // 清空输入
  inputMessage.value = ''

  // 滚动到底部
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }

  // 模拟AI回复
  setTimeout(() => {
    messages.value.push({
      type: 'ai',
      content: '我理解您的问题，让我来帮您解决...',
      time: new Date().toLocaleString()
    })
  }, 1000)
}

const handleClear = () => {
  inputMessage.value = ''
}

const handleEdit = (row: any) => {
  ElMessage.success(`编辑知识: ${row.title}`)
}

const handleTrain = (row: any) => {
  ElMessage.success(`训练知识: ${row.title}`)
}

const handleDelete = (row: any) => {
  ElMessage.success(`删除知识: ${row.title}`)
}

onMounted(() => {
  // 初始化滚动到底部
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
})
</script>

<style scoped>
.ai-assistant {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-overview {
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

.chat-area {
  display: flex;
  flex-direction: column;
  height: 600px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
}

.message-item {
  margin-bottom: 20px;
}

.message-content {
  display: flex;
  align-items: flex-start;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  margin: 0 12px;
}

.message-text {
  max-width: 70%;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.message-body {
  padding: 12px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.user-message .message-body {
  background-color: #ecf5ff;
}

.chat-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.knowledge-content {
  padding: 20px;
}
</style> 