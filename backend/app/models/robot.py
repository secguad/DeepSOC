from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class RobotConfig(Base):
    __tablename__ = "robot_configs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False, comment="机器人类型：feishu/dingtalk/wecom")
    enabled = Column(Boolean, default=False, comment="是否启用")
    webhook = Column(String(512), nullable=True, comment="Webhook地址")
    config = Column(JSON, nullable=True, comment="其他配置信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 