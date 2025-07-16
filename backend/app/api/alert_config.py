from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session
from app.models.alert_config import AlertConfig
from app.schemas.alert_config import AlertConfigCreate, AlertConfigUpdate, AlertConfigInDB

router = APIRouter()

@router.get("/", response_model=list[AlertConfigInDB])
async def get_alert_configs(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    """获取告警配置列表"""
    result = await db.execute(
        "SELECT * FROM alert_configs ORDER BY created_at DESC LIMIT :limit OFFSET :offset",
        {"limit": limit, "offset": skip}
    )
    configs = result.fetchall()
    return configs

@router.post("/", response_model=AlertConfigInDB)
async def create_alert_config(
    config: AlertConfigCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """创建新告警配置"""
    result = await db.execute(
        """
        INSERT INTO alert_configs (name, description, severity, notification_channels)
        VALUES (:name, :description, :severity, :notification_channels)
        RETURNING *
        """,
        config.dict()
    )
    await db.commit()
    return result.fetchone()

@router.get("/{config_id}", response_model=AlertConfigInDB)
async def get_alert_config(
    config_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """获取单个告警配置"""
    result = await db.execute(
        "SELECT * FROM alert_configs WHERE id = :id",
        {"id": config_id}
    )
    config = result.fetchone()
    if not config:
        raise HTTPException(status_code=404, detail="Alert config not found")
    return config

@router.put("/{config_id}", response_model=AlertConfigInDB)
async def update_alert_config(
    config_id: int,
    config: AlertConfigUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """更新告警配置"""
    result = await db.execute(
        """
        UPDATE alert_configs
        SET name = :name,
            description = :description,
            severity = :severity,
            notification_channels = :notification_channels
        WHERE id = :id
        RETURNING *
        """,
        {**config.dict(), "id": config_id}
    )
    await db.commit()
    updated_config = result.fetchone()
    if not updated_config:
        raise HTTPException(status_code=404, detail="Alert config not found")
    return updated_config

@router.delete("/{config_id}")
async def delete_alert_config(
    config_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """删除告警配置"""
    result = await db.execute(
        "DELETE FROM alert_configs WHERE id = :id RETURNING id",
        {"id": config_id}
    )
    await db.commit()
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Alert config not found")
    return {"message": "Alert config deleted successfully"} 