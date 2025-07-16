from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AlertBase(BaseModel):
    title: str
    content: str
    source: str
    severity: str

class AlertCreate(AlertBase):
    pass

class AlertUpdate(AlertBase):
    pass

class AlertInDB(AlertBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 