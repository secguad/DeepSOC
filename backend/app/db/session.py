from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from contextlib import contextmanager

# 创建同步引擎
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI.replace("postgresql+asyncpg", "postgresql"),
    pool_pre_ping=True,
    pool_size=20,  # 增加连接池大小
    max_overflow=30,  # 增加最大溢出连接数
    pool_timeout=30,  # 设置连接池超时时间
    pool_recycle=1800,  # 设置连接回收时间
    echo=settings.SQLALCHEMY_ECHO,
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # 禁用提交时过期
)

@contextmanager
def get_db() -> Session:
    """获取数据库会话的上下文管理器"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 