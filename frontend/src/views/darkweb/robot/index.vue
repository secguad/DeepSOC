<template>
  <div class="robot-config">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>机器人告警配置</span>
          <el-button type="primary" @click="handleSave">保存配置</el-button>
        </div>
      </template>

      <!-- 飞书机器人配置 -->
      <el-form
        ref="feishuFormRef"
        :model="feishuForm"
        :rules="feishuRules"
        label-width="120px"
        class="robot-form"
      >
        <div class="form-section">
          <div class="section-title">
            <el-icon><ChatDotRound /></el-icon>
            <span>飞书机器人</span>
          </div>
          <el-form-item label="启用状态" prop="enabled">
            <el-switch v-model="feishuForm.enabled" />
          </el-form-item>
          <el-form-item label="Webhook地址" prop="webhook">
            <el-input
              v-model="feishuForm.webhook"
              placeholder="请输入飞书机器人Webhook地址"
              :disabled="!feishuForm.enabled"
            />
          </el-form-item>
          <div class="monitor-mode-section">
            <div class="section-subtitle">
              <el-icon><Monitor /></el-icon>
              <span>监控模式配置</span>
            </div>
            <div class="mode-description">
              <p>选择监控模式：</p>
              <ul>
                <li><strong>历史数据扫描</strong>：定期扫描历史交流数据，适合全面检查历史信息</li>
                <li><strong>实时消息监听</strong>：实时监听频道或群组消息，适合及时发现新信息</li>
              </ul>
            </div>
            <el-form-item label="监控模式" prop="monitorMode">
              <el-radio-group v-model="feishuForm.monitorMode" :disabled="!feishuForm.enabled">
                <el-radio value="history">
                  <el-icon><Timer /></el-icon>
                  历史数据扫描
                </el-radio>
                <el-radio value="realtime">
                  <el-icon><VideoPlay /></el-icon>
                  实时消息监听
                </el-radio>
              </el-radio-group>
            </el-form-item>
            <div v-if="feishuForm.monitorMode === 'history'" class="history-settings">
              <div class="settings-title">
                <el-icon><Setting /></el-icon>
                <span>历史数据扫描设置</span>
              </div>
              <el-form-item label="扫描间隔" prop="scanInterval">
                <el-input-number
                  v-model="feishuForm.scanInterval"
                  :min="1"
                  :max="24"
                  :disabled="!feishuForm.enabled"
                  placeholder="请输入扫描间隔（小时）"
                />
                <span class="unit-text">小时</span>
                <div class="setting-tip">设置多久执行一次历史数据扫描</div>
              </el-form-item>
              <el-form-item label="扫描范围" prop="scanRange">
                <el-input-number
                  v-model="feishuForm.scanRange"
                  :min="1"
                  :max="30"
                  :disabled="!feishuForm.enabled"
                  placeholder="请输入扫描范围（天）"
                />
                <span class="unit-text">天</span>
                <div class="setting-tip">设置扫描最近多少天的历史数据</div>
              </el-form-item>
            </div>
          </div>
          <div class="alert-section">
            <div class="section-subtitle">告警配置</div>
            <el-form-item label="可信度" prop="reliability">
              <el-checkbox-group v-model="feishuForm.reliability" :disabled="!feishuForm.enabled">
                <el-checkbox label="high">高可信度</el-checkbox>
                <el-checkbox label="medium">中可信度</el-checkbox>
                <el-checkbox label="low">低可信度</el-checkbox>
                <el-checkbox label="suspected">疑似泄露</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </div>
          <el-form-item label="信息类型" prop="infoTypes">
            <el-checkbox-group v-model="feishuForm.infoTypes" :disabled="!feishuForm.enabled">
              <el-checkbox label="account">账号密码</el-checkbox>
              <el-checkbox label="document">内部文档</el-checkbox>
              <el-checkbox label="code">源代码</el-checkbox>
              <el-checkbox label="data">业务数据</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </div>
      </el-form>

      <!-- 钉钉机器人配置 -->
      <el-form
        ref="dingtalkFormRef"
        :model="dingtalkForm"
        :rules="dingtalkRules"
        label-width="120px"
        class="robot-form"
      >
        <div class="form-section">
          <div class="section-title">
            <el-icon><ChatDotRound /></el-icon>
            <span>钉钉机器人</span>
          </div>
          <el-form-item label="启用状态" prop="enabled">
            <el-switch v-model="dingtalkForm.enabled" />
          </el-form-item>
          <el-form-item label="Webhook地址" prop="webhook">
            <el-input
              v-model="dingtalkForm.webhook"
              placeholder="请输入钉钉机器人Webhook地址"
              :disabled="!dingtalkForm.enabled"
            />
          </el-form-item>
          <div class="monitor-mode-section">
            <div class="section-subtitle">监控模式配置</div>
            <el-form-item label="监控模式" prop="monitorMode">
              <el-radio-group v-model="dingtalkForm.monitorMode" :disabled="!dingtalkForm.enabled">
                <el-radio value="history">历史数据扫描</el-radio>
                <el-radio value="realtime">实时消息监听</el-radio>
              </el-radio-group>
            </el-form-item>
            <div v-if="dingtalkForm.monitorMode === 'history'" class="history-settings">
              <el-form-item label="扫描间隔" prop="scanInterval">
                <el-input-number
                  v-model="dingtalkForm.scanInterval"
                  :min="1"
                  :max="24"
                  :disabled="!dingtalkForm.enabled"
                  placeholder="请输入扫描间隔（小时）"
                />
                <span class="unit-text">小时</span>
              </el-form-item>
              <el-form-item label="扫描范围" prop="scanRange">
                <el-input-number
                  v-model="dingtalkForm.scanRange"
                  :min="1"
                  :max="30"
                  :disabled="!dingtalkForm.enabled"
                  placeholder="请输入扫描范围（天）"
                />
                <span class="unit-text">天</span>
              </el-form-item>
            </div>
          </div>
          <div class="security-section">
            <div class="section-subtitle">安全配置</div>
            <el-form-item label="安全设置" prop="security">
              <el-checkbox-group v-model="dingtalkForm.security" :disabled="!dingtalkForm.enabled">
                <el-checkbox label="sign">加签</el-checkbox>
                <el-checkbox label="ip">IP地址段</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="加签密钥" prop="signKey" v-if="dingtalkForm.security.includes('sign')">
              <el-input
                v-model="dingtalkForm.signKey"
                placeholder="请输入加签密钥"
                :disabled="!dingtalkForm.enabled"
              />
            </el-form-item>
            <el-form-item label="IP地址段" prop="ipList" v-if="dingtalkForm.security.includes('ip')">
              <el-input
                v-model="dingtalkForm.ipList"
                type="textarea"
                :rows="3"
                placeholder="请输入IP地址段，多个地址用逗号分隔"
                :disabled="!dingtalkForm.enabled"
              />
            </el-form-item>
          </div>
          <div class="alert-section">
            <div class="section-subtitle">告警配置</div>
            <el-form-item label="可信度" prop="reliability">
              <el-checkbox-group v-model="dingtalkForm.reliability" :disabled="!dingtalkForm.enabled">
                <el-checkbox label="high">高可信度</el-checkbox>
                <el-checkbox label="medium">中可信度</el-checkbox>
                <el-checkbox label="low">低可信度</el-checkbox>
                <el-checkbox label="suspected">疑似泄露</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </div>
        </div>
      </el-form>

      <!-- 企业微信机器人配置 -->
      <el-form
        ref="wecomFormRef"
        :model="wecomForm"
        :rules="wecomRules"
        label-width="120px"
        class="robot-form"
      >
        <div class="form-section">
          <div class="section-title">
            <el-icon><ChatDotRound /></el-icon>
            <span>企业微信机器人</span>
          </div>
          <el-form-item label="启用状态" prop="enabled">
            <el-switch v-model="wecomForm.enabled" />
          </el-form-item>
          <el-form-item label="Webhook地址" prop="webhook">
            <el-input
              v-model="wecomForm.webhook"
              placeholder="请输入企业微信机器人Webhook地址"
              :disabled="!wecomForm.enabled"
            />
          </el-form-item>
          <div class="monitor-mode-section">
            <div class="section-subtitle">监控模式配置</div>
            <el-form-item label="监控模式" prop="monitorMode">
              <el-radio-group v-model="wecomForm.monitorMode" :disabled="!wecomForm.enabled">
                <el-radio value="history">历史数据扫描</el-radio>
                <el-radio value="realtime">实时消息监听</el-radio>
              </el-radio-group>
            </el-form-item>
            <div v-if="wecomForm.monitorMode === 'history'" class="history-settings">
              <el-form-item label="扫描间隔" prop="scanInterval">
                <el-input-number
                  v-model="wecomForm.scanInterval"
                  :min="1"
                  :max="24"
                  :disabled="!wecomForm.enabled"
                  placeholder="请输入扫描间隔（小时）"
                />
                <span class="unit-text">小时</span>
              </el-form-item>
              <el-form-item label="扫描范围" prop="scanRange">
                <el-input-number
                  v-model="wecomForm.scanRange"
                  :min="1"
                  :max="30"
                  :disabled="!wecomForm.enabled"
                  placeholder="请输入扫描范围（天）"
                />
                <span class="unit-text">天</span>
              </el-form-item>
            </div>
          </div>
          <div class="alert-section">
            <div class="section-subtitle">告警配置</div>
            <el-form-item label="可信度" prop="reliability">
              <el-checkbox-group v-model="wecomForm.reliability" :disabled="!wecomForm.enabled">
                <el-checkbox label="high">高可信度</el-checkbox>
                <el-checkbox label="medium">中可信度</el-checkbox>
                <el-checkbox label="low">低可信度</el-checkbox>
                <el-checkbox label="suspected">疑似泄露</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </div>
          <el-form-item label="消息类型" prop="messageType">
            <el-radio-group v-model="wecomForm.messageType" :disabled="!wecomForm.enabled">
              <el-radio value="text">文本消息</el-radio>
              <el-radio value="markdown">Markdown</el-radio>
            </el-radio-group>
          </el-form-item>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { ChatDotRound, Monitor, Timer, VideoPlay, Setting } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import axios from 'axios'

// API基础URL
const API_BASE_URL = '/api/v1'

// 飞书表单
const feishuFormRef = ref<FormInstance>()
const feishuForm = reactive({
  enabled: false,
  webhook: '',
  monitorMode: 'realtime',
  scanInterval: 24,
  scanRange: 7,
  reliability: ['high', 'medium'],
  infoTypes: ['account', 'document']
})

// 钉钉表单
const dingtalkFormRef = ref<FormInstance>()
const dingtalkForm = reactive({
  enabled: false,
  webhook: '',
  monitorMode: 'realtime',
  scanInterval: 24,
  scanRange: 7,
  security: [] as string[],
  signKey: '',
  ipList: '',
  reliability: ['high', 'medium']
})

// 企业微信表单
const wecomFormRef = ref<FormInstance>()
const wecomForm = reactive({
  enabled: false,
  webhook: '',
  monitorMode: 'realtime',
  scanInterval: 24,
  scanRange: 7,
  reliability: ['high', 'medium'],
  messageType: 'text'
})

// 表单验证规则
const feishuRules = {
  webhook: [
    { required: true, message: '请输入飞书机器人Webhook地址', trigger: 'blur' }
  ],
  monitorMode: [
    { required: true, message: '请选择监控模式', trigger: 'change' }
  ],
  scanInterval: [
    { required: true, message: '请输入扫描间隔', trigger: 'blur' }
  ],
  scanRange: [
    { required: true, message: '请输入扫描范围', trigger: 'blur' }
  ],
  reliability: [
    { required: true, message: '请至少选择一个可信度', trigger: 'change' }
  ],
  infoTypes: [
    { required: true, message: '请至少选择一个信息类型', trigger: 'change' }
  ]
}

const dingtalkRules = {
  webhook: [
    { required: true, message: '请输入钉钉机器人Webhook地址', trigger: 'blur' }
  ],
  monitorMode: [
    { required: true, message: '请选择监控模式', trigger: 'change' }
  ],
  scanInterval: [
    { required: true, message: '请输入扫描间隔', trigger: 'blur' }
  ],
  scanRange: [
    { required: true, message: '请输入扫描范围', trigger: 'blur' }
  ],
  signKey: [
    { required: true, message: '请输入加签密钥', trigger: 'blur' }
  ],
  ipList: [
    { required: true, message: '请输入IP地址段', trigger: 'blur' }
  ],
  reliability: [
    { required: true, message: '请至少选择一个可信度', trigger: 'change' }
  ]
}

const wecomRules = {
  webhook: [
    { required: true, message: '请输入企业微信机器人Webhook地址', trigger: 'blur' }
  ],
  monitorMode: [
    { required: true, message: '请选择监控模式', trigger: 'change' }
  ],
  scanInterval: [
    { required: true, message: '请输入扫描间隔', trigger: 'blur' }
  ],
  scanRange: [
    { required: true, message: '请输入扫描范围', trigger: 'blur' }
  ],
  reliability: [
    { required: true, message: '请至少选择一个可信度', trigger: 'change' }
  ]
}

// 获取机器人配置
const fetchRobotConfigs = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/robot`)
    const configs = response.data

    // 更新飞书配置
    const feishuConfig = configs.find((config: any) => config.type === 'feishu')
    if (feishuConfig) {
      feishuForm.enabled = feishuConfig.enabled
      feishuForm.webhook = feishuConfig.webhook
      if (feishuConfig.config) {
        feishuForm.monitorMode = feishuConfig.config.monitorMode || 'realtime'
        feishuForm.scanInterval = feishuConfig.config.scanInterval || 24
        feishuForm.scanRange = feishuConfig.config.scanRange || 7
        feishuForm.reliability = feishuConfig.config.reliability || ['high', 'medium']
        feishuForm.infoTypes = feishuConfig.config.infoTypes || ['account', 'document']
      }
    }

    // 更新钉钉配置
    const dingtalkConfig = configs.find((config: any) => config.type === 'dingtalk')
    if (dingtalkConfig) {
      dingtalkForm.enabled = dingtalkConfig.enabled
      dingtalkForm.webhook = dingtalkConfig.webhook
      if (dingtalkConfig.config) {
        dingtalkForm.monitorMode = dingtalkConfig.config.monitorMode || 'realtime'
        dingtalkForm.scanInterval = dingtalkConfig.config.scanInterval || 24
        dingtalkForm.scanRange = dingtalkConfig.config.scanRange || 7
        dingtalkForm.security = dingtalkConfig.config.security || []
        dingtalkForm.signKey = dingtalkConfig.config.signKey || ''
        dingtalkForm.ipList = dingtalkConfig.config.ipList || ''
        dingtalkForm.reliability = dingtalkConfig.config.reliability || ['high', 'medium']
      }
    }

    // 更新企业微信配置
    const wecomConfig = configs.find((config: any) => config.type === 'wecom')
    if (wecomConfig) {
      wecomForm.enabled = wecomConfig.enabled
      wecomForm.webhook = wecomConfig.webhook
      if (wecomConfig.config) {
        wecomForm.monitorMode = wecomConfig.config.monitorMode || 'realtime'
        wecomForm.scanInterval = wecomConfig.config.scanInterval || 24
        wecomForm.scanRange = wecomConfig.config.scanRange || 7
        wecomForm.reliability = wecomConfig.config.reliability || ['high', 'medium']
        wecomForm.messageType = wecomConfig.config.messageType || 'text'
      }
    }
  } catch (error) {
    console.error('获取机器人配置失败:', error)
    ElMessage.error('获取机器人配置失败')
  }
}

// 保存配置
const handleSave = async () => {
  try {
    // 验证飞书表单
    if (feishuForm.enabled) {
      await feishuFormRef.value?.validate()
    }

    // 验证钉钉表单
    if (dingtalkForm.enabled) {
      await dingtalkFormRef.value?.validate()
    }

    // 验证企业微信表单
    if (wecomForm.enabled) {
      await wecomFormRef.value?.validate()
    }

    // 保存飞书配置
    if (feishuForm.enabled) {
      await axios.put(`${API_BASE_URL}/robot/feishu`, {
        type: 'feishu',
        enabled: true,
        webhook: feishuForm.webhook,
        config: {
          monitorMode: feishuForm.monitorMode,
          scanInterval: feishuForm.scanInterval,
          scanRange: feishuForm.scanRange,
          reliability: feishuForm.reliability,
          infoTypes: feishuForm.infoTypes
        }
      })
    } else {
      await axios.put(`${API_BASE_URL}/robot/feishu`, {
        type: 'feishu',
        enabled: false
      })
    }

    // 保存钉钉配置
    if (dingtalkForm.enabled) {
      await axios.put(`${API_BASE_URL}/robot/dingtalk`, {
        type: 'dingtalk',
        enabled: true,
        webhook: dingtalkForm.webhook,
        config: {
          monitorMode: dingtalkForm.monitorMode,
          scanInterval: dingtalkForm.scanInterval,
          scanRange: dingtalkForm.scanRange,
          security: dingtalkForm.security,
          signKey: dingtalkForm.signKey,
          ipList: dingtalkForm.ipList,
          reliability: dingtalkForm.reliability
        }
      })
    } else {
      await axios.put(`${API_BASE_URL}/robot/dingtalk`, {
        type: 'dingtalk',
        enabled: false
      })
    }

    // 保存企业微信配置
    if (wecomForm.enabled) {
      await axios.put(`${API_BASE_URL}/robot/wecom`, {
        type: 'wecom',
        enabled: true,
        webhook: wecomForm.webhook,
        config: {
          monitorMode: wecomForm.monitorMode,
          scanInterval: wecomForm.scanInterval,
          scanRange: wecomForm.scanRange,
          reliability: wecomForm.reliability,
          messageType: wecomForm.messageType
        }
      })
    } else {
      await axios.put(`${API_BASE_URL}/robot/wecom`, {
        type: 'wecom',
        enabled: false
      })
    }

    ElMessage.success('配置保存成功')
  } catch (error) {
    console.error('保存配置失败:', error)
    ElMessage.error('保存配置失败')
  }
}

// 页面加载时获取配置
onMounted(() => {
  fetchRobotConfigs()
})
</script>

<style scoped>
.robot-config {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-section {
  margin-bottom: 40px;
  padding: 20px;
  border: 1px solid #EBEEF5;
  border-radius: 4px;
}

.section-title {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.section-title .el-icon {
  margin-right: 8px;
  font-size: 18px;
}

.robot-form {
  max-width: 800px;
}

.monitor-mode-section,
.alert-section,
.security-section {
  margin: 20px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.section-subtitle {
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: bold;
  color: #606266;
  margin-bottom: 15px;
  padding-left: 8px;
  border-left: 3px solid #409EFF;
}

.section-subtitle .el-icon {
  margin-right: 8px;
  color: #409EFF;
}

.history-settings {
  margin-top: 15px;
  padding: 15px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px dashed #DCDFE6;
}

.unit-text {
  margin-left: 8px;
  color: #606266;
}

.mode-description {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #E4E7ED;
}

.mode-description p {
  margin: 0 0 10px 0;
  color: #606266;
  font-weight: bold;
}

.mode-description ul {
  margin: 0;
  padding-left: 20px;
  color: #606266;
}

.mode-description li {
  margin: 5px 0;
  line-height: 1.5;
}

.settings-title {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  color: #606266;
  font-weight: bold;
}

.settings-title .el-icon {
  margin-right: 8px;
  color: #409EFF;
}

.setting-tip {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
}

.el-radio-group .el-radio {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.el-radio-group .el-icon {
  margin-right: 4px;
  font-size: 16px;
}
</style> 