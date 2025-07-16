from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class RobotConfigBase(BaseModel):
    type: str = Field(..., description="机器人类型：feishu/dingtalk/wecom")
    enabled: bool = Field(False, description="是否启用")
    webhook: Optional[str] = Field(None, description="Webhook地址")
    config: Optional[Dict[str, Any]] = Field(None, description="其他配置信息")

class RobotConfigCreate(RobotConfigBase):
    pass

class RobotConfigUpdate(RobotConfigBase):
    pass

class RobotConfigInDB(RobotConfigBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RobotConfigResponse(RobotConfigInDB):
    pass 