from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session
from app.models.keyword import Keyword
from app.schemas.keyword import KeywordCreate, KeywordUpdate, KeywordInDB

router = APIRouter()

@router.get("/", response_model=list[KeywordInDB])
async def get_keywords(
    db: AsyncSession = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    """获取关键词列表"""
    result = await db.execute(
        "SELECT * FROM keywords ORDER BY created_at DESC LIMIT :limit OFFSET :offset",
        {"limit": limit, "offset": skip}
    )
    keywords = result.fetchall()
    return keywords

@router.post("/", response_model=KeywordInDB)
async def create_keyword(
    keyword: KeywordCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """创建新关键词"""
    result = await db.execute(
        """
        INSERT INTO keywords (word, category, description)
        VALUES (:word, :category, :description)
        RETURNING *
        """,
        keyword.dict()
    )
    await db.commit()
    return result.fetchone()

@router.get("/{keyword_id}", response_model=KeywordInDB)
async def get_keyword(
    keyword_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """获取单个关键词"""
    result = await db.execute(
        "SELECT * FROM keywords WHERE id = :id",
        {"id": keyword_id}
    )
    keyword = result.fetchone()
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword

@router.put("/{keyword_id}", response_model=KeywordInDB)
async def update_keyword(
    keyword_id: int,
    keyword: KeywordUpdate,
    db: AsyncSession = Depends(get_db_session)
):
    """更新关键词"""
    result = await db.execute(
        """
        UPDATE keywords
        SET word = :word,
            category = :category,
            description = :description
        WHERE id = :id
        RETURNING *
        """,
        {**keyword.dict(), "id": keyword_id}
    )
    await db.commit()
    updated_keyword = result.fetchone()
    if not updated_keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return updated_keyword

@router.delete("/{keyword_id}")
async def delete_keyword(
    keyword_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """删除关键词"""
    result = await db.execute(
        "DELETE FROM keywords WHERE id = :id RETURNING id",
        {"id": keyword_id}
    )
    await db.commit()
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Keyword not found")
    return {"message": "Keyword deleted successfully"} 