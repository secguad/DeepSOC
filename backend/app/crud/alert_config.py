from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.alert_config import AlertConfig
from app.schemas.alert_config import AlertConfigCreate, AlertConfigUpdate

class CRUDAlertConfig(CRUDBase[AlertConfig, AlertConfigCreate, AlertConfigUpdate]):
    def get_by_channel_id(self, db: Session, *, channel_id: str) -> Optional[AlertConfig]:
        """根据渠道ID获取告警配置"""
        return db.query(AlertConfig).filter(AlertConfig.channel_id == channel_id).first()

    def get_active_configs(self, db: Session) -> List[AlertConfig]:
        """获取所有激活的告警配置"""
        return db.query(AlertConfig).filter(AlertConfig.is_active == True).all()

alert_config = CRUDAlertConfig(AlertConfig) 