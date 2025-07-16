from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float
from app.db.session import Base

class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(100))
    severity = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Keyword(Base):
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    word = Column(String(100), nullable=False, unique=True)
    description = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AIConfig(Base):
    __tablename__ = 'ai_configs'
    
    id = Column(Integer, primary_key=True)
    api_key = Column(String(200), nullable=False)
    model_name = Column(String(100))
    max_tokens = Column(Integer, default=1000)
    temperature = Column(Float, default=0.7)
    created_at = Column(DateTime, default=datetime.utcnow)

class AlertConfig(Base):
    __tablename__ = 'alert_configs'
    
    id = Column(Integer, primary_key=True)
    platform = Column(String(50), nullable=False)  # feishu, dingtalk, wecom
    webhook_url = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TelegramConfig(Base):
    __tablename__ = 'telegram_configs'
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(String(100), nullable=False)
    channel_name = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow) 