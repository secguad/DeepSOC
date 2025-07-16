from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.base_class import Base

class AIConfig(Base):
    __tablename__ = "ai_configs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    api_key = Column(String(200), nullable=False)
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=2000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 