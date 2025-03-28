from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Keyword(BaseModel):
    """关键词模型"""
    id: Optional[int] = None
    word: str
    category: str
    risk_level: str
    description: Optional[str] = None
    created_by: str
    created_at: Optional[datetime] = None
    updated_by: str
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 