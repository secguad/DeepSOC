from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.robot import RobotConfig
from app.schemas.robot import RobotConfigCreate, RobotConfigUpdate

def get_robot_config(db: Session, robot_type: str) -> Optional[RobotConfig]:
    return db.query(RobotConfig).filter(RobotConfig.type == robot_type).first()

def get_all_robot_configs(db: Session) -> List[RobotConfig]:
    return db.query(RobotConfig).all()

def create_robot_config(db: Session, robot_config: RobotConfigCreate) -> RobotConfig:
    db_robot = RobotConfig(**robot_config.model_dump())
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot

def update_robot_config(db: Session, robot_type: str, robot_config: RobotConfigUpdate) -> Optional[RobotConfig]:
    db_robot = get_robot_config(db, robot_type)
    if db_robot:
        for key, value in robot_config.model_dump(exclude_unset=True).items():
            setattr(db_robot, key, value)
        db.commit()
        db.refresh(db_robot)
    return db_robot

def delete_robot_config(db: Session, robot_type: str) -> bool:
    db_robot = get_robot_config(db, robot_type)
    if db_robot:
        db.delete(db_robot)
        db.commit()
        return True
    return False 