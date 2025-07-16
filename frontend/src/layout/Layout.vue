<template>
  <div class="app-wrapper">
    <div class="sidebar-container" :class="{ collapse: isCollapse }">
      <div class="logo">
        <span>DeepSOC</span>
      </div>
      <el-scrollbar>
        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapse"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
          mode="vertical"
          router
        >
          <el-sub-menu index="/security-posture">
            <template #title>
              <el-icon><Monitor /></el-icon>
              <span>安全态势</span>
            </template>
            <el-menu-item index="/dashboard">
              <el-icon><DataLine /></el-icon>
              <span>安全态势仪表盘</span>
            </el-menu-item>
            <el-menu-item index="/score">
              <el-icon><PieChart /></el-icon>
              <span>安全量化评分</span>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/security-defense">
            <template #title>
              <el-icon><Menu /></el-icon>
              <span>安全防御</span>
            </template>
            <el-menu-item index="/security-defense/vulnerability">
              <el-icon><Warning /></el-icon>
              <span>漏洞管理</span>
            </el-menu-item>
            <el-menu-item index="/security-defense/baseline">
              <el-icon><List /></el-icon>
              <span>基线核查</span>
            </el-menu-item>
            <el-menu-item index="/security-defense/waf">
              <el-icon><Link /></el-icon>
              <span>WAF防护</span>
            </el-menu-item>
            <el-menu-item index="/security-defense/attack-surface">
              <el-icon><Aim /></el-icon>
              <span>攻击面测绘</span>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/threat-detection">
            <template #title>
              <el-icon><Aim /></el-icon>
              <span>威胁检测</span>
            </template>
            <el-menu-item index="/threat-detection/ids">
              <el-icon><Search /></el-icon>
              <span>入侵检测</span>
            </el-menu-item>
            <el-menu-item index="/threat-detection/honeypot">
              <el-icon><Box /></el-icon>
              <span>蜜罐诱捕</span>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/incident-response">
            <template #title>
              <el-icon><Clock /></el-icon>
              <span>事件响应</span>
            </template>
            <el-menu-item index="/incident-response/alerts">
              <el-icon><Bell /></el-icon>
              <span>告警处理</span>
            </el-menu-item>
            <el-menu-item index="/incident-response/cases">
              <el-icon><Document /></el-icon>
              <span>事件调查</span>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/assets">
            <template #title>
              <el-icon><Collection /></el-icon>
              <span>安全资产</span>
            </template>
            <el-menu-item index="/assets/inventory">
              <el-icon><Files /></el-icon>
              <span>资产清单</span>
            </el-menu-item>
            <el-menu-item index="/assets/risk">
              <el-icon><InfoFilled /></el-icon>
              <span>风险评估</span>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/darkweb">
            <template #title>
              <el-icon><Monitor /></el-icon>
              <span>暗网监控</span>
            </template>
            <el-menu-item index="/darkweb/dashboard">
              <el-icon><DataLine /></el-icon>
              <span>仪表盘</span>
            </el-menu-item>
            <el-sub-menu index="/darkweb/monitor">
              <template #title>
                <el-icon><Monitor /></el-icon>
                <span>监控配置</span>
              </template>
              <el-menu-item index="/darkweb/monitor/history">
                <el-icon><Timer /></el-icon>
                <span>历史数据扫描</span>
              </el-menu-item>
              <el-menu-item index="/darkweb/monitor/realtime">
                <el-icon><VideoPlay /></el-icon>
                <span>实时消息监听</span>
              </el-menu-item>
            </el-sub-menu>
            <el-menu-item index="/darkweb/keywords">
              <el-icon><Edit /></el-icon>
              <span>关键词管理</span>
            </el-menu-item>
            <el-menu-item index="/darkweb/robot">
              <el-icon><Bell /></el-icon>
              <span>告警配置</span>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/data-security">
            <template #title>
              <el-icon><Money /></el-icon>
              <span>数据安全</span>
            </template>
            <el-menu-item index="/data-security/classify">
              <el-icon><Files /></el-icon>
              <span>数据分类</span>
            </el-menu-item>
            <el-menu-item index="/data-security/protect">
              <el-icon><Lock /></el-icon>
              <span>数据防护</span>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/ueba">
            <template #title>
              <el-icon><User /></el-icon>
              <span>UEBA</span>
            </template>
            <el-menu-item index="/ueba/behavior">
              <el-icon><Operation /></el-icon>
              <span>行为分析</span>
            </el-menu-item>
            <el-menu-item index="/ueba/anomaly">
              <el-icon><Warning /></el-icon>
              <span>异常检测</span>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/ai-assistant">
            <template #title>
              <el-icon><ChatDotRound /></el-icon>
              <span>AI助手</span>
            </template>
            <el-menu-item index="/ai-assistant/chat">
              <el-icon><ChatLineRound /></el-icon>
              <span>智能对话</span>
            </el-menu-item>
            <el-menu-item index="/ai-assistant/analysis">
              <el-icon><DataAnalysis /></el-icon>
              <span>智能分析</span>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="/system">
            <template #title>
              <el-icon><Setting /></el-icon>
              <span>系统管理</span>
            </template>
            <el-menu-item index="/system/users">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
            <el-menu-item index="/system/roles">
              <el-icon><UserFilled /></el-icon>
              <span>角色管理</span>
            </el-menu-item>
            <el-menu-item index="/system/permissions">
              <el-icon><Lock /></el-icon>
              <span>权限管理</span>
            </el-menu-item>
            <el-menu-item index="/system/audit">
              <el-icon><Document /></el-icon>
              <span>操作审计</span>
            </el-menu-item>
            <el-menu-item index="/system/metrics">
              <el-icon><DataLine /></el-icon>
              <span>运营指标</span>
            </el-menu-item>
            <el-menu-item index="/system/logs">
              <el-icon><Document /></el-icon>
              <span>系统日志</span>
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-scrollbar>
    </div>
    
    <div class="main-container">
      <div class="header">
        <div class="left">
          <el-icon class="toggle-sidebar" @click="toggleSidebar">
            <Expand v-if="isCollapse" />
            <Fold v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item>首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ route.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="right">
          <el-dropdown>
            <span class="dropdown-trigger">
              管理员 <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人信息</el-dropdown-item>
                <el-dropdown-item>修改密码</el-dropdown-item>
                <el-dropdown-item divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      <div class="app-main">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  Monitor,
  DataLine,
  PieChart,
  Menu,
  Warning,
  List,
  Link,
  Aim,
  Search,
  Box,
  Clock,
  Bell,
  Document,
  Collection,
  Files,
  InfoFilled,
  Edit,
  DataAnalysis,
  Setting,
  Money,
  Lock,
  User,
  Operation,
  ChatDotRound,
  ChatLineRound,
  UserFilled,
  Expand,
  Fold,
  ArrowDown,
  Timer,
  VideoPlay
} from '@element-plus/icons-vue'

const route = useRoute()
const isCollapse = ref(false)

const activeMenu = computed(() => {
  return route.path
})

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}
</script>

<style scoped>
.app-wrapper {
  height: 100%;
  display: flex;
}

.sidebar-container {
  width: 210px;
  height: 100%;
  background: #304156;
  transition: width 0.3s;
  overflow: hidden;
}

.sidebar-container.collapse {
  width: 64px;
}

.logo {
  height: 50px;
  line-height: 50px;
  text-align: center;
  background: #2b2f3a;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  height: 50px;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.left {
  display: flex;
  align-items: center;
}

.toggle-sidebar {
  font-size: 20px;
  cursor: pointer;
  margin-right: 20px;
}

.dropdown-trigger {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.app-main {
  flex: 1;
  padding: 20px;
  background: #f0f2f5;
  overflow: auto;
}

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-menu--collapse) {
  width: 64px;
}

:deep(.el-menu-item), :deep(.el-sub-menu__title) {
  height: 50px;
  line-height: 50px;
}
</style> 