<template>
  <div class="waf">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>WAF防护</span>
          <div class="header-actions">
            <el-switch
              v-model="wafEnabled"
              active-text="已启用"
              inactive-text="已禁用"
              @change="handleWafSwitch"
            />
            <el-button type="primary" style="margin-left: 16px">配置规则</el-button>
          </div>
        </div>
      </template>
      
      <div class="statistics">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>今日拦截</span>
                  <el-tag type="danger">高</el-tag>
                </div>
              </template>
              <div class="stat-number">1,234</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>本周拦截</span>
                  <el-tag type="warning">中</el-tag>
                </div>
              </template>
              <div class="stat-number">8,567</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>本月拦截</span>
                  <el-tag type="info">低</el-tag>
                </div>
              </template>
              <div class="stat-number">32,198</div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>防护规则</span>
                </div>
              </template>
              <div class="stat-number">156</div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div class="content">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="time" label="时间" width="180" />
          <el-table-column prop="ip" label="攻击源IP" width="150" />
          <el-table-column prop="type" label="攻击类型" width="150">
            <template #default="scope">
              <el-tag :type="getAttackType(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="url" label="目标URL" />
          <el-table-column prop="action" label="处理动作" width="100">
            <template #default="scope">
              <el-tag :type="getActionType(scope.row.action)">
                {{ scope.row.action }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="danger" link @click="handleBlock(scope.row)">
                封禁
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const wafEnabled = ref(true)

const tableData = ref([
  {
    time: '2024-02-20 10:00:00',
    ip: '192.168.1.100',
    type: 'SQL注入',
    url: '/api/users',
    action: '拦截'
  },
  {
    time: '2024-02-20 10:05:00',
    ip: '192.168.1.101',
    type: 'XSS攻击',
    url: '/api/comments',
    action: '告警'
  },
  {
    time: '2024-02-20 10:10:00',
    ip: '192.168.1.102',
    type: '目录遍历',
    url: '/api/files',
    action: '拦截'
  }
])

const getAttackType = (type: string) => {
  const types = {
    'SQL注入': 'danger',
    'XSS攻击': 'warning',
    '目录遍历': 'info'
  }
  return types[type] || 'info'
}

const getActionType = (action: string) => {
  const types = {
    '拦截': 'danger',
    '告警': 'warning',
    '放行': 'success'
  }
  return types[action] || 'info'
}

const handleWafSwitch = (value: boolean) => {
  console.log('WAF状态切换:', value)
}

const handleDetail = (row: any) => {
  console.log('查看详情:', row)
}

const handleBlock = (row: any) => {
  console.log('封禁IP:', row)
}
</script>

<style scoped>
.waf {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
}

.statistics {
  margin-bottom: 20px;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  text-align: center;
  margin-top: 10px;
}

.content {
  margin-top: 20px;
}
</style> 