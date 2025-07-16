from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AIConfigBase(BaseModel):
    model_name: str
    api_key: str
    temperature: float
    max_tokens: int

class AIConfigCreate(AIConfigBase):
    pass

class AIConfigUpdate(AIConfigBase):
    pass

class AIConfigInDB(AIConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 