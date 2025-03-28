<template>
  <div class="honeypot">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>蜜罐诱捕</span>
          <div class="header-actions">
            <el-button type="success">部署蜜罐</el-button>
            <el-button type="primary" style="margin-left: 16px">配置管理</el-button>
          </div>
        </div>
      </template>

      <div class="statistics">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>蜜罐总数</span>
                </div>
              </template>
              <div class="stat-content">
                <div class="stat-number">12</div>
                <div class="stat-detail">
                  <el-tag type="success">运行: 10</el-tag>
                  <el-tag type="danger">停止: 2</el-tag>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>今日攻击</span>
                </div>
              </template>
              <div class="stat-content">
                <div class="stat-number">156</div>
                <div class="stat-detail">
                  <span>较昨日</span>
                  <span class="trend-up">+23%</span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>攻击源IP</span>
                </div>
              </template>
              <div class="stat-content">
                <div class="stat-number">45</div>
                <div class="stat-detail">
                  <span>已封禁</span>
                  <el-tag type="danger">23</el-tag>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <template #header>
                <div class="stat-header">
                  <span>样本采集</span>
                </div>
              </template>
              <div class="stat-content">
                <div class="stat-number">89</div>
                <div class="stat-detail">
                  <span>恶意文件</span>
                  <el-tag type="warning">34</el-tag>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div class="honeypot-list">
        <el-table :data="honeypotList" style="width: 100%">
          <el-table-column prop="name" label="蜜罐名称" />
          <el-table-column prop="type" label="类型" width="120">
            <template #default="scope">
              <el-tag>{{ scope.row.type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="ip" label="IP地址" width="150" />
          <el-table-column prop="port" label="端口" width="100" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="attacks" label="攻击次数" width="100" />
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleDetail(scope.row)">
                详情
              </el-button>
              <el-button type="success" link @click="handleLogs(scope.row)">
                日志
              </el-button>
              <el-button type="warning" link @click="handleConfig(scope.row)">
                配置
              </el-button>
              <el-button type="danger" link @click="handleDelete(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="attack-logs">
        <div class="section-header">
          <h3>最新攻击日志</h3>
          <el-button type="primary" link>查看更多</el-button>
        </div>
        <el-table :data="attackLogs" style="width: 100%">
          <el-table-column prop="time" label="时间" width="180" />
          <el-table-column prop="honeypot" label="蜜罐" width="120" />
          <el-table-column prop="source" label="攻击源" width="150" />
          <el-table-column prop="type" label="攻击类型" width="120">
            <template #default="scope">
              <el-tag :type="getAttackType(scope.row.type)">
                {{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="detail" label="攻击详情" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button type="primary" link @click="handleAttackDetail(scope.row)">
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

const honeypotList = ref([
  {
    name: 'Web蜜罐-1',
    type: 'Web服务',
    ip: '192.168.1.100',
    port: '80',
    status: '运行中',
    attacks: 45
  },
  {
    name: 'SSH蜜罐-1',
    type: 'SSH服务',
    ip: '192.168.1.101',
    port: '22',
    status: '运行中',
    attacks: 78
  },
  {
    name: 'FTP蜜罐-1',
    type: 'FTP服务',
    ip: '192.168.1.102',
    port: '21',
    status: '已停止',
    attacks: 23
  }
])

const attackLogs = ref([
  {
    time: '2024-02-20 10:00:00',
    honeypot: 'Web蜜罐-1',
    source: '192.168.1.200',
    type: 'SQL注入',
    detail: '尝试进行SQL注入攻击，使用常见注入payload'
  },
  {
    time: '2024-02-20 10:05:00',
    honeypot: 'SSH蜜罐-1',
    source: '192.168.1.201',
    type: '暴力破解',
    detail: '尝试使用弱口令字典进行暴力破解'
  },
  {
    time: '2024-02-20 10:10:00',
    honeypot: 'FTP蜜罐-1',
    source: '192.168.1.202',
    type: '未授权访问',
    detail: '尝试匿名登录FTP服务'
  }
])

const getStatusType = (status: string): string => {
  switch (status) {
    case '运行中':
      return 'success'
    case '已停止':
      return 'danger'
    default:
      return 'info'
  }
}

const getAttackType = (type: string): string => {
  switch (type) {
    case 'SQL注入':
      return 'danger'
    case '暴力破解':
      return 'warning'
    case '未授权访问':
      return 'info'
    default:
      return 'info'
  }
}

const handleDetail = (row: any) => {
  console.log('查看蜜罐详情:', row)
}

const handleLogs = (row: any) => {
  console.log('查看蜜罐日志:', row)
}

const handleConfig = (row: any) => {
  console.log('配置蜜罐:', row)
}

const handleDelete = (row: any) => {
  console.log('删除蜜罐:', row)
}

const handleAttackDetail = (row: any) => {
  console.log('查看攻击详情:', row)
}

const handleBlock = (row: any) => {
  console.log('封禁IP:', row)
}
</script>

<style scoped>
.honeypot {
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
  text-align: center;
  padding: 10px 0;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.stat-detail {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.trend-up {
  color: #f56c6c;
}

.honeypot-list {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  margin: 0;
}

.attack-logs {
  margin-top: 20px;
}
</style> 