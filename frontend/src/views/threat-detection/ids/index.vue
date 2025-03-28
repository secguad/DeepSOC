<template>
  <div class="ids">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>入侵检测</span>
          <div class="header-actions">
            <el-switch
              v-model="idsEnabled"
              active-text="已启用"
              inactive-text="已禁用"
              @change="handleIdsSwitch"
            />
            <el-button type="primary" style="margin-left: 16px">规则配置</el-button>
          </div>
        </div>
      </template>

      <div class="statistics">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>今日告警</span>
                  <el-tag type="danger">{{ todayAlerts }}</el-tag>
                </div>
              </template>
              <div class="stat-content">
                <div class="stat-item">
                  <span>高危</span>
                  <span class="number danger">45</span>
                </div>
                <div class="stat-item">
                  <span>中危</span>
                  <span class="number warning">78</span>
                </div>
                <div class="stat-item">
                  <span>低危</span>
                  <span class="number info">123</span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>检测规则</span>
                </div>
              </template>
              <div class="stat-content">
                <div class="stat-item">
                  <span>已启用</span>
                  <span class="number success">156</span>
                </div>
                <div class="stat-item">
                  <span>未启用</span>
                  <span class="number info">24</span>
                </div>
                <div class="stat-item">
                  <span>总数</span>
                  <span class="number">180</span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>检测引擎</span>
                </div>
              </template>
              <div class="stat-content">
                <div class="stat-item">
                  <span>运行状态</span>
                  <el-tag type="success">正常</el-tag>
                </div>
                <div class="stat-item">
                  <span>CPU使用率</span>
                  <el-progress :percentage="45" />
                </div>
                <div class="stat-item">
                  <span>内存使用率</span>
                  <el-progress :percentage="65" type="warning" />
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div class="content">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="time" label="时间" width="180" />
          <el-table-column prop="source" label="来源IP" width="150" />
          <el-table-column prop="destination" label="目的IP" width="150" />
          <el-table-column prop="type" label="攻击类型" width="150">
            <template #default="scope">
              <el-tag :type="getAlertType(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="level" label="危险等级" width="100">
            <template #default="scope">
              <el-tag :type="getLevelType(scope.row.level)">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleProcess(scope.row)">
                处理
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
import { ref, computed } from 'vue'

const idsEnabled = ref(true)
const todayAlerts = computed(() => 246)

const tableData = ref([
  {
    time: '2024-02-20 10:00:00',
    source: '192.168.1.100',
    destination: '192.168.1.1',
    type: '暴力破解',
    level: '高危',
    status: '未处理'
  },
  {
    time: '2024-02-20 10:05:00',
    source: '192.168.1.101',
    destination: '192.168.1.2',
    type: '异常连接',
    level: '中危',
    status: '处理中'
  },
  {
    time: '2024-02-20 10:10:00',
    source: '192.168.1.102',
    destination: '192.168.1.3',
    type: '端口扫描',
    level: '低危',
    status: '已处理'
  }
])

const getAlertType = (type: string): string => {
  switch (type) {
    case '暴力破解':
      return 'danger'
    case '异常连接':
      return 'warning'
    case '端口扫描':
      return 'info'
    default:
      return 'info'
  }
}

const getLevelType = (level: string): string => {
  switch (level) {
    case '高危':
      return 'danger'
    case '中危':
      return 'warning'
    case '低危':
      return 'info'
    default:
      return 'info'
  }
}

const getStatusType = (status: string): string => {
  switch (status) {
    case '未处理':
      return 'danger'
    case '处理中':
      return 'warning'
    case '已处理':
      return 'success'
    default:
      return 'info'
  }
}

const handleIdsSwitch = (value: boolean) => {
  console.log('IDS状态切换:', value)
}

const handleDetail = (row: any) => {
  console.log('查看详情:', row)
}

const handleProcess = (row: any) => {
  console.log('处理告警:', row)
}

const handleBlock = (row: any) => {
  console.log('封禁IP:', row)
}
</script>

<style scoped>
.ids {
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

.stat-content {
  padding: 10px 0;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.number {
  font-weight: bold;
  font-size: 18px;
}

.number.danger {
  color: var(--el-color-danger);
}

.number.warning {
  color: var(--el-color-warning);
}

.number.success {
  color: var(--el-color-success);
}

.number.info {
  color: var(--el-color-info);
}

.content {
  margin-top: 20px;
}
</style> 