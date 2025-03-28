from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.telegram_client import TelegramMonitorClient
from app.core.feishu_client import FeishuClient
from app.services.alert_service import AlertService
from app.services.keyword_service import KeywordService
from app.models.alert import Alert
from app.models.keyword import Keyword
from app.config.settings import settings
import asyncio
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="暗网监控系统")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
telegram_client = TelegramMonitorClient()
feishu_client = FeishuClient()
alert_service = AlertService()
keyword_service = KeywordService()

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    await alert_service.init_pool()
    await keyword_service.init_pool()
    asyncio.create_task(telegram_client.start_monitoring())

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理"""
    await alert_service.close_pool()
    await keyword_service.close_pool()
    await telegram_client.stop_monitoring()

@app.get("/")
async def root():
    """根路径"""
    return {"message": "暗网监控系统API"}

@app.get("/keywords")
async def get_keywords(
    category: str = None,
    risk_level: str = None,
    page: int = 1,
    page_size: int = 20
):
    """获取关键词列表"""
    try:
        keywords, total = await keyword_service.get_keywords(
            category=category,
            risk_level=risk_level,
            page=page,
            page_size=page_size
        )
        return {
            "code": 0,
            "message": "success",
            "data": {
                "items": keywords,
                "total": total
            }
        }
    except Exception as e:
        logger.error(f"获取关键词列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/keywords")
async def create_keyword(keyword: Keyword):
    """创建关键词"""
    try:
        keyword_id = await keyword_service.create_keyword(keyword)
        return {
            "code": 0,
            "message": "success",
            "data": {"id": keyword_id}
        }
    except Exception as e:
        logger.error(f"创建关键词失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/keywords/{keyword_id}")
async def update_keyword(keyword_id: int, keyword: Keyword):
    """更新关键词"""
    try:
        keyword.id = keyword_id
        success = await keyword_service.update_keyword(keyword)
        if not success:
            raise HTTPException(status_code=404, detail="关键词不存在")
        return {
            "code": 0,
            "message": "success"
        }
    except Exception as e:
        logger.error(f"更新关键词失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/keywords/{keyword_id}")
async def delete_keyword(keyword_id: int):
    """删除关键词"""
    try:
        success = await keyword_service.delete_keyword(keyword_id)
        if not success:
            raise HTTPException(status_code=404, detail="关键词不存在")
        return {
            "code": 0,
            "message": "success"
        }
    except Exception as e:
        logger.error(f"删除关键词失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts")
async def get_alerts(
    status: str = None,
    risk_level: str = None,
    start_date: str = None,
    end_date: str = None,
    page: int = 1,
    page_size: int = 20
):
    """获取告警列表"""
    try:
        alerts, total = await alert_service.get_alerts(
            status=status,
            risk_level=risk_level,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size
        )
        return {
            "code": 0,
            "message": "success",
            "data": {
                "items": alerts,
                "total": total
            }
        }
    except Exception as e:
        logger.error(f"获取告警列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/alerts/{alert_id}/status")
async def update_alert_status(
    alert_id: int,
    status: str,
    processed_by: str,
    process_comment: str
):
    """更新告警状态"""
    try:
        success = await alert_service.update_alert_status(
            alert_id=alert_id,
            status=status,
            processed_by=processed_by,
            process_comment=process_comment
        )
        if not success:
            raise HTTPException(status_code=404, detail="告警不存在")
        return {
            "code": 0,
            "message": "success"
        }
    except Exception as e:
        logger.error(f"更新告警状态失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 