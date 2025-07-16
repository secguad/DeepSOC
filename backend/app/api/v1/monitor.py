from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import monitor as monitor_crud
from app.schemas.monitor import (
    MonitorChannel,
    MonitorChannelCreate,
    MonitorChannelUpdate,
    MonitorMessage,
    MonitorMessageCreate,
    MonitorMessageUpdate,
    MonitorStatus,
    MessageStats
)

router = APIRouter()

@router.get("/channels", response_model=List[MonitorChannel])
def get_channels(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    return monitor_crud.get_channels(db, skip=skip, limit=limit)

@router.post("/channels", response_model=MonitorChannel)
def create_channel(
    channel: MonitorChannelCreate,
    db: Session = Depends(deps.get_db)
):
    return monitor_crud.create_channel(db, channel_data=channel.dict())

@router.put("/channels/{channel_id}", response_model=MonitorChannel)
def update_channel(
    channel_id: int,
    channel: MonitorChannelUpdate,
    db: Session = Depends(deps.get_db)
):
    db_channel = monitor_crud.update_channel(db, channel_id, channel_data=channel.dict(exclude_unset=True))
    if not db_channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return db_channel

@router.delete("/channels/{channel_id}")
def delete_channel(
    channel_id: int,
    db: Session = Depends(deps.get_db)
):
    success = monitor_crud.delete_channel(db, channel_id)
    if not success:
        raise HTTPException(status_code=404, detail="Channel not found")
    return {"message": "Channel deleted successfully"}

@router.get("/messages", response_model=List[MonitorMessage])
def get_messages(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    channel_id: Optional[int] = None,
    is_ignored: Optional[bool] = None
):
    return monitor_crud.get_messages(db, skip=skip, limit=limit, channel_id=channel_id, is_ignored=is_ignored)

@router.post("/messages", response_model=MonitorMessage)
def create_message(
    message: MonitorMessageCreate,
    db: Session = Depends(deps.get_db)
):
    return monitor_crud.create_message(db, message_data=message.dict())

@router.put("/messages/{message_id}", response_model=MonitorMessage)
def update_message(
    message_id: int,
    message: MonitorMessageUpdate,
    db: Session = Depends(deps.get_db)
):
    db_message = monitor_crud.update_message(db, message_id, message_data=message.dict(exclude_unset=True))
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@router.get("/status", response_model=MonitorStatus)
def get_monitor_status(
    db: Session = Depends(deps.get_db)
):
    status = monitor_crud.get_monitor_status(db)
    if not status:
        status = monitor_crud.update_monitor_status(db, is_monitoring=False)
    return status

@router.post("/status", response_model=MonitorStatus)
def update_monitor_status(
    is_monitoring: bool,
    db: Session = Depends(deps.get_db)
):
    return monitor_crud.update_monitor_status(db, is_monitoring=is_monitoring)

@router.get("/stats", response_model=MessageStats)
def get_message_stats(
    db: Session = Depends(deps.get_db)
):
    return monitor_crud.get_message_stats(db) 