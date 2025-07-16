from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.ai_config import AIConfig
from app.schemas.ai_config import AIConfigCreate, AIConfigUpdate

class CRUDAIConfig(CRUDBase[AIConfig, AIConfigCreate, AIConfigUpdate]):
    def get_active_config(self, db: Session) -> Optional[AIConfig]:
        """获取当前激活的AI配置"""
        return db.query(AIConfig).filter(AIConfig.is_active == True).first()

ai_config = CRUDAIConfig(AIConfig) 