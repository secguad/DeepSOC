from flask import Blueprint
from fastapi import APIRouter

bp = Blueprint('api', __name__)

router = APIRouter()

from app.api import (
    alerts,
    keywords,
    ai_config,
    alert_config,
    telegram_config
)

# 注册路由
router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
router.include_router(keywords.router, prefix="/keywords", tags=["keywords"])
router.include_router(ai_config.router, prefix="/ai-config", tags=["ai-config"])
router.include_router(alert_config.router, prefix="/alert-config", tags=["alert-config"])
router.include_router(telegram_config.router, prefix="/telegram-config", tags=["telegram-config"]) 