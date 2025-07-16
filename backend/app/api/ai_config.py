from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session
from app.models.ai_config import AIConfig
from app.schemas.ai_config import AIConfigCreate, AIConfigUpdate, AIConfigInDB

router = APIRouter()

@router.get("/", response_model=AIConfigInDB)
async def get_ai_config(
    db: AsyncSession = Depends(get_db_session)
):
    """获取 AI 配置"""
    result = await db.execute(
        "SELECT * FROM ai_configs ORDER BY created_at DESC LIMIT 1"
    )
    config = result.fetchone()
    if not config:
        raise HTTPException(status_code=404, detail="AI config not found")
    return config

@router.post("/", response_model=AIConfigInDB)
async def create_ai_config(
    config: AIConfigCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """创建新 AI 配置"""
    result = await db.execute(
        """
        INSERT INTO ai_configs (model_name, api_key, temperature, max_tokens)
        VALUES (:model_name, :api_key, :temperature, :max_tokens)
        RETURNING *
        """,
        config.dict()
    )
    await db.commit()
    return result.fetchone()

@router.put("/{config_id}", response_model=AIConfigInDB)
async def update_ai_config(
    config_id: int,
    config: AIConfigUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """更新 AI 配置"""
    result = await db.execute(
        """
        UPDATE ai_configs
        SET model_name = :model_name,
            api_key = :api_key,
            temperature = :temperature,
            max_tokens = :max_tokens
        WHERE id = :id
        RETURNING *
        """,
        {**config.dict(), "id": config_id}
    )
    await db.commit()
    updated_config = result.fetchone()
    if not updated_config:
        raise HTTPException(status_code=404, detail="AI config not found")
    return updated_config 