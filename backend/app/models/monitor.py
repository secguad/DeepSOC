from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class ChannelType(str, enum.Enum):
    TELEGRAM = "telegram"
    DISCORD = "discord"
    SLACK = "slack"
    EMAIL = "email"
    WEBHOOK = "webhook"

class MonitorStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class ChannelStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"

class MonitorChannel(Base):
    __tablename__ = "monitor_channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    channel_id = Column(String(100), unique=True, nullable=False)
    status = Column(Enum(MonitorStatus), default=MonitorStatus.INACTIVE)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_check_time = Column(DateTime)
    error_message = Column(Text)
    
    messages = relationship("MonitorMessage", back_populates="channel")

class MonitorMessage(Base):
    __tablename__ = "monitor_messages"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("monitor_channels.id"))
    message_id = Column(String(100), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_processed = Column(Boolean, default=False)
    processing_status = Column(String(50))
    error_message = Column(Text)
    
    channel = relationship("MonitorChannel", back_populates="messages")

class MonitorStatus(Base):
    __tablename__ = "monitor_status"

    id = Column(Integer, primary_key=True, index=True)
    is_monitoring = Column(Boolean, default=False)
    start_time = Column(DateTime)
    last_update = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime) 