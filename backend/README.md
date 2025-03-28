# 暗网监控系统后端

这是一个基于FastAPI的暗网监控系统后端服务，用于监控Telegram频道和群组中的敏感信息。

## 功能特点

- 关键词管理：支持添加、修改、删除和查询关键词
- 告警管理：支持查看和处理告警信息
- Telegram监控：自动监控指定频道和群组
- 飞书通知：支持将告警信息发送到飞书机器人

## 技术栈

- FastAPI：Web框架
- SQLAlchemy：ORM框架
- Telethon：Telegram客户端
- MySQL：数据库
- Pydantic：数据验证

## 安装

1. 克隆代码库：
```bash
git clone <repository_url>
cd backend
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑.env文件，填入必要的配置信息
```

5. 初始化数据库：
```bash
mysql -u root -p < app/db/init_db.sql
```

## 运行

启动开发服务器：
```bash
uvicorn app.main:app --reload
```

访问API文档：
- Swagger UI：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

## API接口

### 关键词管理

- GET /keywords：获取关键词列表
- POST /keywords：创建关键词
- PUT /keywords/{keyword_id}：更新关键词
- DELETE /keywords/{keyword_id}：删除关键词

### 告警管理

- GET /alerts：获取告警列表
- PUT /alerts/{alert_id}/status：更新告警状态

## 配置说明

### 数据库配置

- DB_HOST：数据库主机地址
- DB_PORT：数据库端口
- DB_USER：数据库用户名
- DB_PASSWORD：数据库密码
- DB_NAME：数据库名称

### Telegram配置

- TELEGRAM_API_ID：Telegram API ID
- TELEGRAM_API_HASH：Telegram API Hash
- TELEGRAM_BOT_TOKEN：Telegram机器人Token
- TELEGRAM_CHANNELS：要监控的频道列表
- TELEGRAM_GROUPS：要监控的群组列表

### 飞书配置

- FEISHU_WEBHOOK_URL：飞书机器人Webhook地址

### 监控配置

- MONITOR_INTERVAL：监控间隔（秒）
- KEYWORD_MATCH_THRESHOLD：关键词匹配阈值

## 开发指南

### 项目结构

```
backend/
├── app/
│   ├── config/         # 配置文件
│   ├── core/           # 核心功能
│   ├── db/             # 数据库相关
│   ├── models/         # 数据模型
│   ├── services/       # 业务服务
│   └── main.py         # 应用入口
├── requirements.txt    # 依赖文件
└── README.md          # 项目说明
```

### 添加新功能

1. 在`models`目录下创建数据模型
2. 在`services`目录下创建服务类
3. 在`main.py`中添加API路由
4. 更新数据库结构（如果需要）

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License 