from typing import Any, Dict, Optional
import os
from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DeepSOC"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "deepsoc"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_ECHO: bool = False

    # 安全配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # 监控配置
    MONITOR_INTERVAL: int = 300  # 5 minutes
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30

    # OCR配置
    TESSERACT_CMD: str = "tesseract"  # Linux/macOS默认路径

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"

    # 监控配置
    MONITOR_ERROR_INTERVAL: int = 60  # 错误重试间隔（秒）
    MONITOR_RELIABILITY_THRESHOLD: float = 0.7  # 可信度阈值
    
    # Telegram配置
    TELEGRAM_API_ID: str = "your-api-id"
    TELEGRAM_API_HASH: str = "your-api-hash"
    TELEGRAM_PHONE: Optional[str] = None
    
    # 关键词配置
    KEYWORDS_FILE: str = "keywords.txt"
    
    # 代理配置
    PROXY_ENABLED: bool = False
    PROXY_URL: Optional[str] = None
    
    # 机器人配置
    FEISHU_WEBHOOK: Optional[str] = None
    DINGTALK_WEBHOOK: Optional[str] = None
    WECHAT_WEBHOOK: Optional[str] = None
    
    # 根据操作系统设置默认路径
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.name == 'nt':  # Windows系统
            self.TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 