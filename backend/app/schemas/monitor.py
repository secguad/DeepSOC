from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.monitor import ChannelType, ChannelStatus

class MonitorChannelBase(BaseModel):
    name: str
    type: ChannelType
    description: Optional[str] = None

class MonitorChannelCreate(MonitorChannelBase):
    pass

class MonitorChannelUpdate(MonitorChannelBase):
    name: Optional[str] = None
    type: Optional[ChannelType] = None
    status: Optional[ChannelStatus] = None

class MonitorChannel(MonitorChannelBase):
    id: int
    status: ChannelStatus
    last_update: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MonitorMessageBase(BaseModel):
    channel_id: int
    time: datetime
    source: str
    content: str
    reliability: str
    url: Optional[str] = None
    screenshot: Optional[str] = None

class MonitorMessageCreate(MonitorMessageBase):
    pass

class MonitorMessageUpdate(BaseModel):
    is_ignored: Optional[bool] = None
    reliability: Optional[str] = None
    url: Optional[str] = None
    screenshot: Optional[str] = None

class MonitorMessage(MonitorMessageBase):
    id: int
    is_new: bool
    is_ignored: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MonitorStatus(BaseModel):
    id: int
    is_monitoring: bool
    start_time: Optional[datetime]
    last_update: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MessageStats(BaseModel):
    total: int
    high: int
    medium: int
    low: int 