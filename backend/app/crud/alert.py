from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate

class CRUDAlert(CRUDBase[Alert, AlertCreate, AlertUpdate]):
    def get_by_channel_id(self, db: Session, *, channel_id: str) -> List[Alert]:
        """根据渠道ID获取告警列表"""
        return db.query(Alert).filter(Alert.channel_id == channel_id).all()

    def get_unread(self, db: Session) -> List[Alert]:
        """获取未读告警列表"""
        return db.query(Alert).filter(Alert.is_read == False).all()

    def mark_as_read(self, db: Session, *, alert_id: int) -> Alert:
        """标记告警为已读"""
        alert = self.get(db, id=alert_id)
        if alert:
            alert.is_read = True
            db.commit()
            db.refresh(alert)
        return alert

alert = CRUDAlert(Alert) 