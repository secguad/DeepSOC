from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.telegram_config import TelegramConfig
from app.schemas.telegram_config import TelegramConfigCreate, TelegramConfigUpdate

class CRUDTelegramConfig(CRUDBase[TelegramConfig, TelegramConfigCreate, TelegramConfigUpdate]):
    def get_active_config(self, db: Session) -> Optional[TelegramConfig]:
        """获取当前激活的Telegram配置"""
        return db.query(TelegramConfig).filter(TelegramConfig.is_active == True).first()

telegram_config = CRUDTelegramConfig(TelegramConfig) 