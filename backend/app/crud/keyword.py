from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.keyword import Keyword
from app.schemas.keyword import KeywordCreate, KeywordUpdate
from app.crud.base import CRUDBase

class CRUDKeyword(CRUDBase[Keyword, KeywordCreate, KeywordUpdate]):
    def get_by_word(self, db: Session, *, word: str) -> Optional[Keyword]:
        """根据关键词内容获取关键词"""
        return db.query(Keyword).filter(Keyword.word == word).first()

    def get_active_keywords(self, db: Session) -> List[Keyword]:
        """获取所有激活的关键词"""
        return db.query(Keyword).filter(Keyword.is_active == True).all()

    def count(self, db: Session) -> int:
        """获取关键词总数"""
        return db.query(Keyword).count()

    def get_keywords(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        word: Optional[str] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Keyword]:
        """获取关键词列表"""
        query = db.query(Keyword)
        
        if word:
            query = query.filter(
                or_(
                    Keyword.word.ilike(f"%{word}%"),
                    Keyword.description.ilike(f"%{word}%")
                )
            )
        if category:
            query = query.filter(Keyword.category == category)
        if is_active is not None:
            query = query.filter(Keyword.is_active == is_active)
            
        return query.order_by(Keyword.created_at.desc()).offset(skip).limit(limit).all()

keyword = CRUDKeyword(Keyword) 