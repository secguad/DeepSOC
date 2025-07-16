from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.base_class import Base

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False, unique=True, index=True)
    category = Column(String(50), nullable=False)
    description = Column(String(500))
    is_active = Column(Boolean, default=True)
    match_count = Column(Integer, default=0)
    last_match_time = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now()) 