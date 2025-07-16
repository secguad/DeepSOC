from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import robot as robot_crud
from app.schemas.robot import RobotConfigCreate, RobotConfigUpdate, RobotConfigResponse

router = APIRouter()

@router.get("/", response_model=List[RobotConfigResponse])
def get_robot_configs(
    db: Session = Depends(deps.get_db)
):
    """获取所有机器人配置"""
    return robot_crud.get_all_robot_configs(db)

@router.get("/{robot_type}", response_model=RobotConfigResponse)
def get_robot_config(
    robot_type: str,
    db: Session = Depends(deps.get_db)
):
    """获取指定类型的机器人配置"""
    robot_config = robot_crud.get_robot_config(db, robot_type)
    if not robot_config:
        raise HTTPException(status_code=404, detail="Robot config not found")
    return robot_config

@router.post("/", response_model=RobotConfigResponse)
def create_robot_config(
    robot_config: RobotConfigCreate,
    db: Session = Depends(deps.get_db)
):
    """创建机器人配置"""
    return robot_crud.create_robot_config(db, robot_config)

@router.put("/{robot_type}", response_model=RobotConfigResponse)
def update_robot_config(
    robot_type: str,
    robot_config: RobotConfigUpdate,
    db: Session = Depends(deps.get_db)
):
    """更新机器人配置"""
    updated_config = robot_crud.update_robot_config(db, robot_type, robot_config)
    if not updated_config:
        raise HTTPException(status_code=404, detail="Robot config not found")
    return updated_config

@router.delete("/{robot_type}")
def delete_robot_config(
    robot_type: str,
    db: Session = Depends(deps.get_db)
):
    """删除机器人配置"""
    success = robot_crud.delete_robot_config(db, robot_type)
    if not success:
        raise HTTPException(status_code=404, detail="Robot config not found")
    return {"message": "Robot config deleted successfully"} 