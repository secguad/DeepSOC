from typing import Optional
from pydantic import BaseModel, Field, constr, validator
from datetime import datetime

class KeywordBase(BaseModel):
    word: constr(min_length=2, max_length=100) = Field(..., description="关键词内容")
    category: str = Field(..., description="关键词类型", pattern="^(company|product|domain|ip)$")
    description: Optional[constr(max_length=500)] = Field(None, description="关键词描述")
    is_active: bool = Field(True, description="是否启用")

class KeywordCreate(KeywordBase):
    pass

class KeywordUpdate(KeywordBase):
    word: Optional[constr(min_length=2, max_length=100)] = None
    category: Optional[str] = Field(None, pattern="^(company|product|domain|ip)$")
    is_active: Optional[bool] = None

class KeywordResponse(KeywordBase):
    id: int
    match_count: Optional[int] = 0
    last_match_time: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class KeywordInDB(KeywordBase):
    id: int
    match_count: Optional[int] = 0
    last_match_time: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Keyword(KeywordInDB):
    pass 