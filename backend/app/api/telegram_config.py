from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session
from app.models.telegram_config import TelegramConfig
from app.schemas.telegram_config import TelegramConfigCreate, TelegramConfigUpdate, TelegramConfigInDB

router = APIRouter()

@router.get("/", response_model=TelegramConfigInDB)
async def get_telegram_config(
    db: AsyncSession = Depends(get_db_session)
):
    """获取 Telegram 配置"""
    result = await db.execute(
        "SELECT * FROM telegram_configs ORDER BY created_at DESC LIMIT 1"
    )
    config = result.fetchone()
    if not config:
        raise HTTPException(status_code=404, detail="Telegram config not found")
    return config

@router.post("/", response_model=TelegramConfigInDB)
async def create_telegram_config(
    config: TelegramConfigCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """创建新 Telegram 配置"""
    result = await db.execute(
        """
        INSERT INTO telegram_configs (bot_token, chat_id, enabled)
        VALUES (:bot_token, :chat_id, :enabled)
        RETURNING *
        """,
        config.dict()
    )
    await db.commit()
    return result.fetchone()

@router.put("/{config_id}", response_model=TelegramConfigInDB)
async def update_telegram_config(
    config_id: int,
    config: TelegramConfigUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """更新 Telegram 配置"""
    result = await db.execute(
        """
        UPDATE telegram_configs
        SET bot_token = :bot_token,
            chat_id = :chat_id,
            enabled = :enabled
        WHERE id = :id
        RETURNING *
        """,
        {**config.dict(), "id": config_id}
    )
    await db.commit()
    updated_config = result.fetchone()
    if not updated_config:
        raise HTTPException(status_code=404, detail="Telegram config not found")
    return updated_config 