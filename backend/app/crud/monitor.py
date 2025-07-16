from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.monitor import MonitorChannel, MonitorMessage, MonitorStatus, ChannelStatus
from app.schemas.monitor import MonitorChannelCreate, MonitorChannelUpdate
from datetime import datetime

def get_channel(db: Session, channel_id: int) -> Optional[MonitorChannel]:
    return db.query(MonitorChannel).filter(MonitorChannel.id == channel_id).first()

def get_channels(db: Session, skip: int = 0, limit: int = 100) -> List[MonitorChannel]:
    return db.query(MonitorChannel).offset(skip).limit(limit).all()

def create_channel(db: Session, channel_data: dict) -> MonitorChannel:
    db_channel = MonitorChannel(
        name=channel_data["name"],
        type=channel_data["type"],
        description=channel_data.get("description"),
        status=ChannelStatus.INACTIVE,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

def update_channel(db: Session, channel_id: int, channel_data: dict) -> Optional[MonitorChannel]:
    db_channel = get_channel(db, channel_id)
    if db_channel:
        for key, value in channel_data.items():
            setattr(db_channel, key, value)
        db_channel.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_channel)
    return db_channel

def delete_channel(db: Session, channel_id: int) -> bool:
    db_channel = get_channel(db, channel_id)
    if db_channel:
        db.delete(db_channel)
        db.commit()
        return True
    return False

def get_messages(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    channel_id: Optional[int] = None,
    is_ignored: Optional[bool] = None
) -> List[MonitorMessage]:
    query = db.query(MonitorMessage)
    if channel_id:
        query = query.filter(MonitorMessage.channel_id == channel_id)
    if is_ignored is not None:
        query = query.filter(MonitorMessage.is_ignored == is_ignored)
    return query.order_by(MonitorMessage.time.desc()).offset(skip).limit(limit).all()

def create_message(db: Session, message_data: dict) -> MonitorMessage:
    db_message = MonitorMessage(
        channel_id=message_data["channel_id"],
        time=message_data["time"],
        source=message_data["source"],
        content=message_data["content"],
        reliability=message_data["reliability"],
        url=message_data.get("url"),
        screenshot=message_data.get("screenshot"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def update_message(db: Session, message_id: int, message_data: dict) -> Optional[MonitorMessage]:
    db_message = db.query(MonitorMessage).filter(MonitorMessage.id == message_id).first()
    if db_message:
        for key, value in message_data.items():
            setattr(db_message, key, value)
        db_message.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_message)
    return db_message

def get_monitor_status(db: Session) -> Optional[MonitorStatus]:
    return db.query(MonitorStatus).first()

def update_monitor_status(db: Session, is_monitoring: bool) -> MonitorStatus:
    status = get_monitor_status(db)
    if not status:
        status = MonitorStatus()
        db.add(status)
    
    status.is_monitoring = is_monitoring
    if is_monitoring:
        status.start_time = datetime.utcnow()
    status.last_update = datetime.utcnow()
    status.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(status)
    return status

def get_message_stats(db: Session) -> dict:
    today = datetime.utcnow().date()
    total = db.query(MonitorMessage).filter(
        MonitorMessage.time >= today
    ).count()
    
    high = db.query(MonitorMessage).filter(
        MonitorMessage.time >= today,
        MonitorMessage.reliability == "高"
    ).count()
    
    medium = db.query(MonitorMessage).filter(
        MonitorMessage.time >= today,
        MonitorMessage.reliability == "中"
    ).count()
    
    low = db.query(MonitorMessage).filter(
        MonitorMessage.time >= today,
        MonitorMessage.reliability == "低"
    ).count()
    
    return {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low
    }

class CRUDMonitor(CRUDBase[MonitorChannel, MonitorChannelCreate, MonitorChannelUpdate]):
    def get_by_channel_id(self, db: Session, *, channel_id: str) -> Optional[MonitorChannel]:
        """根据渠道ID获取监控渠道"""
        return db.query(MonitorChannel).filter(MonitorChannel.channel_id == channel_id).first()

    def get_active_channels(self, db: Session) -> List[MonitorChannel]:
        """获取所有激活的监控渠道"""
        return db.query(MonitorChannel).filter(MonitorChannel.is_active == True).all()

monitor = CRUDMonitor(MonitorChannel) 