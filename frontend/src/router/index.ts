import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../layout/Layout.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/dashboard/index.vue'),
        meta: { title: '安全态势仪表盘' }
      },
      {
        path: 'score',
        name: 'Score',
        component: () => import('../views/score/index.vue'),
        meta: { title: '安全量化评分' }
      }
    ]
  },
  {
    path: '/security-defense',
    component: Layout,
    meta: { title: '安全防御' },
    children: [
      {
        path: 'vulnerability',
        name: 'Vulnerability',
        component: () => import('../views/security-defense/vulnerability/index.vue'),
        meta: { title: '漏洞管理' }
      },
      {
        path: 'baseline',
        name: 'Baseline',
        component: () => import('../views/security-defense/baseline/index.vue'),
        meta: { title: '基线核查' }
      },
      {
        path: 'waf',
        name: 'WAF',
        component: () => import('../views/security-defense/waf/index.vue'),
        meta: { title: 'WAF防护' }
      },
      {
        path: 'attack-surface',
        name: 'AttackSurface',
        component: () => import('../views/security-defense/attack-surface/index.vue'),
        meta: { title: '攻击面测绘' }
      }
    ]
  },
  {
    path: '/threat-detection',
    component: Layout,
    meta: { title: '威胁检测' },
    children: [
      {
        path: 'ids',
        name: 'IDS',
        component: () => import('../views/threat-detection/ids/index.vue'),
        meta: { title: '入侵检测' }
      },
      {
        path: 'honeypot',
        name: 'Honeypot',
        component: () => import('../views/threat-detection/honeypot/index.vue'),
        meta: { title: '蜜罐诱捕' }
      }
    ]
  },
  {
    path: '/incident-response',
    component: Layout,
    meta: { title: '事件响应' },
    children: [
      {
        path: 'alerts',
        name: 'Alerts',
        component: () => import('../views/incident-response/alerts/index.vue'),
        meta: { title: '告警处理' }
      },
      {
        path: 'cases',
        name: 'Cases',
        component: () => import('../views/incident-response/cases/index.vue'),
        meta: { title: '事件调查' }
      }
    ]
  },
  {
    path: '/assets',
    component: Layout,
    meta: { title: '安全资产' },
    children: [
      {
        path: 'inventory',
        name: 'Inventory',
        component: () => import('../views/assets/inventory/index.vue'),
        meta: { title: '资产清单' }
      },
      {
        path: 'risk',
        name: 'Risk',
        component: () => import('../views/assets/risk/index.vue'),
        meta: { title: '风险评估' }
      }
    ]
  },
  {
    path: '/darkweb',
    component: Layout,
    meta: { title: '暗网监控' },
    children: [
      {
        path: 'monitor',
        name: 'DarkwebMonitor',
        component: () => import('../views/darkweb/monitor/index.vue'),
        meta: { title: '暗网监控' }
      },
      {
        path: 'keywords',
        name: 'DarkwebKeywords',
        component: () => import('../views/darkweb/keywords/index.vue'),
        meta: { title: '关键词管理' }
      },
      {
        path: 'alerts',
        name: 'DarkwebAlerts',
        component: () => import('../views/darkweb/alerts/index.vue'),
        meta: { title: '告警管理' }
      },
      {
        path: 'analysis',
        name: 'DarkwebAnalysis',
        component: () => import('../views/darkweb/analysis/index.vue'),
        meta: { title: '数据分析' }
      }
    ]
  },
  {
    path: '/data-security',
    component: Layout,
    meta: { title: '数据安全' },
    children: [
      {
        path: 'classify',
        name: 'DataClassify',
        component: () => import('../views/data-security/classify/index.vue'),
        meta: { title: '数据分类' }
      },
      {
        path: 'protect',
        name: 'DataProtect',
        component: () => import('../views/data-security/protect/index.vue'),
        meta: { title: '数据防护' }
      }
    ]
  },
  {
    path: '/ueba',
    component: Layout,
    meta: { title: 'UEBA' },
    children: [
      {
        path: 'behavior',
        name: 'Behavior',
        component: () => import('../views/ueba/behavior/index.vue'),
        meta: { title: '行为分析' }
      },
      {
        path: 'anomaly',
        name: 'Anomaly',
        component: () => import('../views/ueba/anomaly/index.vue'),
        meta: { title: '异常检测' }
      }
    ]
  },
  {
    path: '/ai-assistant',
    component: Layout,
    meta: { title: 'AI助手' },
    children: [
      {
        path: 'chat',
        name: 'Chat',
        component: () => import('../views/ai-assistant/chat/index.vue'),
        meta: { title: '智能对话' }
      },
      {
        path: 'analysis',
        name: 'AIAnalysis',
        component: () => import('../views/ai-assistant/analysis/index.vue'),
        meta: { title: '智能分析' }
      }
    ]
  },
  {
    path: '/system',
    component: Layout,
    meta: { title: '系统管理' },
    children: [
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/system/users/index.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: 'roles',
        name: 'Roles',
        component: () => import('../views/system/roles/index.vue'),
        meta: { title: '角色权限' }
      },
      {
        path: 'logs',
        name: 'Logs',
        component: () => import('../views/system/logs/index.vue'),
        meta: { title: '系统日志' }
      },
      {
        path: 'system',
        name: 'System',
        component: () => import('../views/system/index.vue'),
        meta: { title: '系统管理' },
        children: [
          {
            path: 'users',
            name: 'Users',
            component: () => import('../views/system/users/index.vue'),
            meta: { title: '用户管理' }
          },
          {
            path: 'roles',
            name: 'Roles',
            component: () => import('../views/system/roles/index.vue'),
            meta: { title: '角色管理' }
          },
          {
            path: 'permissions',
            name: 'Permissions',
            component: () => import('../views/system/permissions/index.vue'),
            meta: { title: '权限管理' }
          },
          {
            path: 'audit',
            name: 'Audit',
            component: () => import('../views/system/audit/index.vue'),
            meta: { title: '操作审计' }
          },
          {
            path: 'metrics',
            name: 'Metrics',
            component: () => import('../views/system/metrics/index.vue'),
            meta: { title: '运营指标' }
          },
          {
            path: 'logs',
            name: 'Logs',
            component: () => import('../views/system/logs/index.vue'),
            meta: { title: '系统日志' }
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 