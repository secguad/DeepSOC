from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.base_class import Base

class TelegramConfig(Base):
    __tablename__ = "telegram_configs"

    id = Column(Integer, primary_key=True, index=True)
    bot_token = Column(String(200), nullable=False)
    chat_id = Column(String(100), nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 