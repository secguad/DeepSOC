<template>
  <div class="chat">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>智能对话</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleNewChat">新建对话</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出记录</el-button>
          </div>
        </div>
      </template>

      <!-- 对话区域 -->
      <div class="chat-container">
        <div class="chat-messages" ref="messagesContainer">
          <div v-for="(message, index) in messages" :key="index" class="message-item">
            <div class="message-avatar">
              <el-avatar :size="40" :src="message.role === 'user' ? userAvatar : aiAvatar" />
            </div>
            <div class="message-content">
              <div class="message-role">{{ message.role === 'user' ? '我' : 'AI助手' }}</div>
              <div class="message-text">{{ message.content }}</div>
              <div class="message-time">{{ message.time }}</div>
            </div>
          </div>
        </div>
        <div class="chat-input">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题..."
            @keydown.ctrl.enter="handleSend"
          />
          <div class="input-actions">
            <el-button type="primary" @click="handleSend">发送</el-button>
            <el-button @click="handleClear">清空</el-button>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'

// 用户和AI头像
const userAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
const aiAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

// 消息列表
const messages = ref([
  {
    role: 'user',
    content: '你好，请帮我分析一下最近的安全事件。',
    time: '2024-02-20 10:00:00'
  },
  {
    role: 'assistant',
    content: '好的，我来帮您分析最近的安全事件。根据系统记录，过去24小时内发现以下异常：\n1. 3次异常登录尝试\n2. 2次敏感数据访问\n3. 1次系统配置变更\n\n建议您重点关注这些异常行为，我可以帮您进一步分析具体细节。',
    time: '2024-02-20 10:00:05'
  }
])

const inputMessage = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const handleSend = () => {
  if (!inputMessage.value.trim()) return

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: inputMessage.value,
    time: new Date().toLocaleString()
  })

  // 模拟AI回复
  setTimeout(() => {
    messages.value.push({
      role: 'assistant',
      content: '我理解您的问题，让我来为您解答...',
      time: new Date().toLocaleString()
    })
    scrollToBottom()
  }, 1000)

  inputMessage.value = ''
  scrollToBottom()
}

const handleClear = () => {
  inputMessage.value = ''
}

const handleNewChat = () => {
  messages.value = []
  ElMessage.success('已开始新的对话')
}

const handleExport = () => {
  ElMessage.success('导出对话记录...')
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.chat {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);
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
  display: flex;
  margin-bottom: 20px;
}

.message-avatar {
  margin-right: 12px;
}

.message-content {
  flex: 1;
  background-color: #fff;
  padding: 12px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.message-role {
  font-weight: bold;
  margin-bottom: 4px;
  color: #303133;
}

.message-text {
  color: #606266;
  white-space: pre-wrap;
  line-height: 1.5;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  text-align: right;
}

.chat-input {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}
</style> 