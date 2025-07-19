# DeepSOC - 深度安全运营中心

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/vue-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.109+-red.svg)](https://fastapi.tiangolo.com/)

DeepSOC是一个现代化的安全运营中心(Security Operations Center)系统，提供全面的安全态势感知、威胁检测、事件响应和暗网监控功能。

## 🌟 主要功能

### 🔍 安全态势感知
- **安全态势仪表盘**: 实时监控安全事件趋势和关键指标
- **安全量化评分**: 多维度安全评分体系，量化安全状态
- **安全指标管理**: 自定义安全指标和权重配置

### 🛡️ 安全防御
- **漏洞管理**: 漏洞扫描、评估、修复跟踪
- **基线核查**: 安全基线配置检查和合规性评估
- **WAF防护**: Web应用防火墙配置和监控
- **攻击面测绘**: 资产发现、端口扫描、服务识别

### 🚨 威胁检测
- **入侵检测(IDS)**: 网络流量异常检测和告警
- **蜜罐诱捕**: 主动诱捕攻击者，收集威胁情报

### ⚡ 事件响应
- **告警处理**: 安全事件告警管理和处理流程
- **事件调查**: 安全事件详细分析和取证

### 🌐 暗网监控
- **实时监控**: Telegram频道和群组实时消息监听
- **历史扫描**: 历史数据分析和关键词匹配
- **关键词管理**: 自定义监控关键词和风险等级
- **告警配置**: 多渠道告警通知(飞书、钉钉、微信)

### 🔐 数据安全
- **数据分类**: 敏感数据识别和分类管理
- **数据防护**: 数据加密、访问控制、脱敏处理
- **数据备份**: 重要数据备份和恢复管理

### 👥 系统管理
- **用户管理**: 用户账户和权限管理
- **角色权限**: 基于角色的访问控制
- **系统审计**: 操作日志和审计跟踪
- **系统监控**: 系统性能和服务状态监控

## 🏗️ 技术架构

### 后端技术栈
- **框架**: FastAPI + Flask
- **数据库**: PostgreSQL + MySQL
- **ORM**: SQLAlchemy
- **认证**: JWT + OAuth2
- **消息队列**: Redis + Celery
- **搜索引擎**: Elasticsearch
- **监控**: Prometheus + Grafana

### 前端技术栈
- **框架**: Vue 3 + TypeScript
- **UI组件**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **图表**: ECharts
- **构建工具**: Vite

### 核心特性
- **微服务架构**: 模块化设计，易于扩展
- **RESTful API**: 标准化API接口
- **实时通信**: WebSocket实时数据推送
- **容器化部署**: Docker支持
- **CI/CD**: 自动化部署流程

## 📦 安装部署

### 环境要求
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+
- Docker (可选)

### 快速开始

1. **克隆项目**
```bash
git clone https://github.com/your-username/deepsoc.git
cd deepsoc
```

2. **后端部署**
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息

# 初始化数据库
alembic upgrade head

# 启动后端服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

3. **前端部署**
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

4. **Docker部署(推荐)**
```bash
# 使用Docker Compose一键部署
docker-compose up -d
```

## ⚙️ 配置说明

### 环境变量配置

创建 `.env` 文件并配置以下参数：

```env
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost/deepsoc
REDIS_URL=redis://localhost:6379

# 安全配置
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Telegram配置(暗网监控)
TELEGRAM_API_ID=your-api-id
TELEGRAM_API_HASH=your-api-hash
TELEGRAM_PHONE=your-phone-number

# 告警通知配置
FEISHU_WEBHOOK_URL=your-feishu-webhook
DINGTALK_WEBHOOK_URL=your-dingtalk-webhook
WECHAT_WEBHOOK_URL=your-wechat-webhook

# Elasticsearch配置
ES_HOSTS=localhost:9200
ES_USERNAME=elastic
ES_PASSWORD=your-password
```

### 数据库初始化

```sql
-- 创建数据库
CREATE DATABASE deepsoc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 运行迁移脚本
alembic upgrade head
```

## 🚀 使用指南

### 1. 系统登录
访问 `http://localhost:3000` 使用默认账户登录：
- 用户名: admin
- 密码: admin123

### 2. 暗网监控配置
1. 进入"暗网监控"模块
2. 配置Telegram API密钥
3. 添加监控关键词
4. 设置告警通知渠道

### 3. 安全态势监控
1. 查看"安全态势"仪表盘
2. 配置安全指标权重
3. 监控安全评分变化

### 4. 威胁检测
1. 配置IDS规则
2. 部署蜜罐系统
3. 监控异常行为

## 📊 API文档

启动后端服务后，访问以下地址查看API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 主要API端点

```
GET  /api/v1/keywords          # 获取关键词列表
POST /api/v1/keywords          # 创建关键词
PUT  /api/v1/keywords/{id}     # 更新关键词
DELETE /api/v1/keywords/{id}   # 删除关键词

GET  /api/v1/alerts            # 获取告警列表
PUT  /api/v1/alerts/{id}       # 更新告警状态

GET  /api/v1/monitor/status    # 获取监控状态
POST /api/v1/monitor/start     # 启动监控
POST /api/v1/monitor/stop      # 停止监控
```

## 🧪 测试

### 后端测试
```bash
cd backend
pytest tests/ -v
```

### 前端测试
```bash
cd frontend
npm run test
```

## 📈 性能监控

系统集成了Prometheus和Grafana进行性能监控：

- **应用指标**: 请求响应时间、错误率、吞吐量
- **系统指标**: CPU、内存、磁盘使用率
- **业务指标**: 告警数量、处理效率、安全评分

## 🔧 开发指南

### 代码规范
- 使用Black进行Python代码格式化
- 使用ESLint进行JavaScript代码检查
- 遵循PEP 8和Vue.js官方风格指南

### 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

### 分支管理
- `main`: 主分支，用于生产环境
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复分支

## 🤝 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下开源项目的支持：
- [Vue.js](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [ECharts](https://echarts.apache.org/)

## 📞 联系我们

- 项目主页: https://github.com/your-username/deepsoc
- 问题反馈: https://github.com/your-username/deepsoc/issues
- 邮箱: your-email@example.com

---

**DeepSOC** - 让安全运营更智能、更高效！ 🚀 