from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate, AlertInDB

router = APIRouter()

@router.get("/", response_model=list[AlertInDB])
async def get_alerts(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    """获取告警列表"""
    result = await db.execute(
        "SELECT * FROM alerts ORDER BY created_at DESC LIMIT :limit OFFSET :offset",
        {"limit": limit, "offset": skip}
    )
    alerts = result.fetchall()
    return alerts

@router.post("/", response_model=AlertInDB)
async def create_alert(
    alert: AlertCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """创建新告警"""
    result = await db.execute(
        """
        INSERT INTO alerts (title, content, source, severity)
        VALUES (:title, :content, :source, :severity)
        RETURNING *
        """,
        alert.dict()
    )
    await db.commit()
    return result.fetchone()

@router.get("/{alert_id}", response_model=AlertInDB)
async def get_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """获取单个告警"""
    result = await db.execute(
        "SELECT * FROM alerts WHERE id = :id",
        {"id": alert_id}
    )
    alert = result.fetchone()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.put("/{alert_id}", response_model=AlertInDB)
async def update_alert(
    alert_id: int,
    alert: AlertUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """更新告警"""
    result = await db.execute(
        """
        UPDATE alerts
        SET title = :title,
            content = :content,
            source = :source,
            severity = :severity
        WHERE id = :id
        RETURNING *
        """,
        {**alert.dict(), "id": alert_id}
    )
    await db.commit()
    updated_alert = result.fetchone()
    if not updated_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return updated_alert

@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """删除告警"""
    result = await db.execute(
        "DELETE FROM alerts WHERE id = :id RETURNING id",
        {"id": alert_id}
    )
    await db.commit()
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deleted successfully"} 