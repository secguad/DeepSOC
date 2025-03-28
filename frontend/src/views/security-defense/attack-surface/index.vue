<template>
  <div class="attack-surface">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>攻击面测绘</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleScan">开始扫描</el-button>
            <el-button type="success" style="margin-left: 16px" @click="handleExport">导出报告</el-button>
          </div>
        </div>
      </template>

      <!-- 概览统计 -->
      <div class="overview">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">发现资产</div>
                <div class="overview-value">128</div>
                <div class="overview-trend">
                  较上次
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
                <div class="overview-title">开放端口</div>
                <div class="overview-value">256</div>
                <div class="overview-trend">
                  较上次
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
                <div class="overview-title">发现漏洞</div>
                <div class="overview-value">23</div>
                <div class="overview-trend">
                  较上次
                  <span class="down">
                    5
                    <el-icon><ArrowDown /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="overview-item">
                <div class="overview-title">高危资产</div>
                <div class="overview-value">8</div>
                <div class="overview-trend">
                  较上次
                  <span class="down">
                    2
                    <el-icon><ArrowDown /></el-icon>
                  </span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 扫描配置 -->
      <div class="scan-config">
        <div class="section-title">扫描配置</div>
        <el-form :model="scanForm" label-width="120px">
          <el-form-item label="扫描范围">
            <el-input
              v-model="scanForm.targets"
              type="textarea"
              :rows="3"
              placeholder="请输入扫描目标，每行一个"
            />
          </el-form-item>
          <el-form-item label="扫描类型">
            <el-checkbox-group v-model="scanForm.types">
              <el-checkbox label="port">端口扫描</el-checkbox>
              <el-checkbox label="service">服务识别</el-checkbox>
              <el-checkbox label="vulnerability">漏洞扫描</el-checkbox>
              <el-checkbox label="subdomain">子域名发现</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="扫描深度">
            <el-radio-group v-model="scanForm.depth">
              <el-radio label="quick">快速扫描</el-radio>
              <el-radio label="normal">标准扫描</el-radio>
              <el-radio label="deep">深度扫描</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="并发数">
            <el-input-number v-model="scanForm.concurrent" :min="1" :max="10" />
          </el-form-item>
          <el-form-item label="超时时间">
            <el-input-number v-model="scanForm.timeout" :min="30" :max="300" />
            <span class="unit">秒</span>
          </el-form-item>
        </el-form>
      </div>

      <!-- 扫描结果 -->
      <div class="scan-results">
        <div class="section-title">扫描结果</div>
        <el-tabs v-model="activeTab">
          <el-tab-pane label="资产列表" name="assets">
            <el-table :data="assetList" style="width: 100%">
              <el-table-column prop="id" label="ID" width="120" />
              <el-table-column prop="ip" label="IP地址" width="140" />
              <el-table-column prop="domain" label="域名" />
              <el-table-column prop="type" label="资产类型" width="120" />
              <el-table-column prop="ports" label="开放端口" width="120" />
              <el-table-column prop="risk" label="风险等级" width="100">
                <template #default="scope">
                  <el-tag :type="getRiskTag(scope.row.risk)">
                    {{ scope.row.risk }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="updateTime" label="更新时间" width="180" />
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="scope">
                  <el-button type="primary" link @click="handleDetail(scope.row)">
                    详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="漏洞列表" name="vulnerabilities">
            <el-table :data="vulnList" style="width: 100%">
              <el-table-column prop="id" label="ID" width="120" />
              <el-table-column prop="title" label="漏洞名称" />
              <el-table-column prop="type" label="漏洞类型" width="120" />
              <el-table-column prop="level" label="风险等级" width="100">
                <template #default="scope">
                  <el-tag :type="getLevelTag(scope.row.level)">
                    {{ scope.row.level }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="target" label="影响资产" width="140" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="scope">
                  <el-tag :type="getStatusTag(scope.row.status)">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="updateTime" label="更新时间" width="180" />
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="scope">
                  <el-button type="primary" link @click="handleVulnDetail(scope.row)">
                    详情
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>

    <!-- 资产详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="资产详情"
      width="800px"
    >
      <div v-if="currentItem" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentItem.id }}</el-descriptions-item>
          <el-descriptions-item label="IP地址">{{ currentItem.ip }}</el-descriptions-item>
          <el-descriptions-item label="域名">{{ currentItem.domain }}</el-descriptions-item>
          <el-descriptions-item label="资产类型">{{ currentItem.type }}</el-descriptions-item>
          <el-descriptions-item label="开放端口">{{ currentItem.ports }}</el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag :type="getRiskTag(currentItem.risk)">
              {{ currentItem.risk }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="操作系统" :span="2">{{ currentItem.os }}</el-descriptions-item>
          <el-descriptions-item label="服务列表" :span="2">
            <el-table :data="currentItem.services" style="width: 100%">
              <el-table-column prop="port" label="端口" width="100" />
              <el-table-column prop="service" label="服务" width="120" />
              <el-table-column prop="version" label="版本" />
              <el-table-column prop="banner" label="Banner" />
            </el-table>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>

    <!-- 漏洞详情对话框 -->
    <el-dialog
      v-model="vulnDetailVisible"
      title="漏洞详情"
      width="800px"
    >
      <div v-if="currentVuln" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">{{ currentVuln.id }}</el-descriptions-item>
          <el-descriptions-item label="漏洞名称">{{ currentVuln.title }}</el-descriptions-item>
          <el-descriptions-item label="漏洞类型">{{ currentVuln.type }}</el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag :type="getLevelTag(currentVuln.level)">
              {{ currentVuln.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="影响资产">{{ currentVuln.target }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTag(currentVuln.status)">
              {{ currentVuln.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="漏洞描述" :span="2">{{ currentVuln.description }}</el-descriptions-item>
          <el-descriptions-item label="影响范围" :span="2">{{ currentVuln.scope }}</el-descriptions-item>
          <el-descriptions-item label="修复建议" :span="2">{{ currentVuln.solution }}</el-descriptions-item>
          <el-descriptions-item label="参考链接" :span="2">
            <el-link type="primary" :href="currentVuln.reference" target="_blank">
              {{ currentVuln.reference }}
            </el-link>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'

// 扫描表单
const scanForm = ref({
  targets: '',
  types: ['port', 'service'],
  depth: 'normal',
  concurrent: 5,
  timeout: 60
})

// 当前激活的标签页
const activeTab = ref('assets')

// 资产列表数据
const assetList = ref([
  {
    id: 'ASSET-2024-001',
    ip: '192.168.1.100',
    domain: 'example.com',
    type: 'Web服务器',
    ports: '80,443,8080',
    risk: '中',
    os: 'Ubuntu 20.04',
    services: [
      {
        port: '80',
        service: 'HTTP',
        version: 'Apache/2.4.41',
        banner: 'Apache/2.4.41 (Ubuntu)'
      },
      {
        port: '443',
        service: 'HTTPS',
        version: 'Nginx/1.18.0',
        banner: 'Nginx/1.18.0 (Ubuntu)'
      }
    ],
    updateTime: '2024-02-20 10:00:00'
  }
])

// 漏洞列表数据
const vulnList = ref([
  {
    id: 'VULN-2024-001',
    title: 'Apache Log4j 远程代码执行漏洞',
    type: '远程代码执行',
    level: '高危',
    target: '192.168.1.100',
    status: '未修复',
    description: 'Apache Log4j 2.x 版本存在远程代码执行漏洞，攻击者可利用该漏洞在目标服务器上执行任意代码。',
    scope: '影响所有使用 Log4j 2.x 版本的应用',
    solution: '升级 Log4j 到 2.17.0 或更高版本',
    reference: 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44228',
    updateTime: '2024-02-20 10:00:00'
  }
])

const detailVisible = ref(false)
const vulnDetailVisible = ref(false)
const currentItem = ref<any>(null)
const currentVuln = ref<any>(null)

const getRiskTag = (risk: string): string => {
  switch (risk) {
    case '高':
      return 'danger'
    case '中':
      return 'warning'
    case '低':
      return 'info'
    default:
      return ''
  }
}

const getLevelTag = (level: string): string => {
  switch (level) {
    case '高危':
      return 'danger'
    case '中危':
      return 'warning'
    case '低危':
      return 'info'
    default:
      return ''
  }
}

const getStatusTag = (status: string): string => {
  switch (status) {
    case '未修复':
      return 'danger'
    case '修复中':
      return 'warning'
    case '已修复':
      return 'success'
    default:
      return ''
  }
}

const handleScan = () => {
  ElMessage.success('开始扫描')
}

const handleExport = () => {
  ElMessage.success('开始导出报告')
}

const handleDetail = (row: any) => {
  currentItem.value = row
  detailVisible.value = true
}

const handleVulnDetail = (row: any) => {
  currentVuln.value = row
  vulnDetailVisible.value = true
}
</script>

<style scoped>
.attack-surface {
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

.overview {
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

.scan-config {
  margin-bottom: 40px;
}

.unit {
  margin-left: 8px;
  color: #909399;
}

.scan-results {
  margin-top: 20px;
}

.detail-content {
  padding: 20px;
}
</style> 