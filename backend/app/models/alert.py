from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class Alert(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    link: Optional[str] = None
    type: str
    src_site: str
    date: datetime
    keywords: List[str]
    channel_id: str
    channel_name: str
    risk_level: str = "medium"  # low, medium, high
    status: str = "unprocessed"  # unprocessed, processing, processed, ignored
    processed_by: Optional[str] = None
    processed_at: Optional[datetime] = None
    process_comment: Optional[str] = None

    class Config:
        from_attributes = True 