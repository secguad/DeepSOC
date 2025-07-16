from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TelegramConfigBase(BaseModel):
    bot_token: str
    chat_id: str
    enabled: bool

class TelegramConfigCreate(TelegramConfigBase):
    pass

class TelegramConfigUpdate(TelegramConfigBase):
    pass

class TelegramConfigInDB(TelegramConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 