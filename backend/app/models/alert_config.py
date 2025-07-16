from sqlalchemy import Column, Integer, String, Text, DateTime, func, JSON
from app.db.base_class import Base

class AlertConfig(Base):
    __tablename__ = "alert_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    severity = Column(String(20), nullable=False)  # high, medium, low
    notification_channels = Column(JSON, nullable=False)  # List of notification channels
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 