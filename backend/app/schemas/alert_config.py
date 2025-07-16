from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class AlertConfigBase(BaseModel):
    name: str
    description: Optional[str] = None
    severity: str
    notification_channels: List[str]

class AlertConfigCreate(AlertConfigBase):
    pass

class AlertConfigUpdate(AlertConfigBase):
    pass

class AlertConfigInDB(AlertConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 