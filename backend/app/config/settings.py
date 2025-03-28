from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Telegram配置
    TELEGRAM_API_ID: str = '12726421'
    TELEGRAM_API_HASH: str = '7e9094825ae0ea2d17ac6b7f65d10794'
    TELEGRAM_PHONE: str = '+8613301075221'
    
    # 目标频道ID列表
    TELEGRAM_TARGET_CHANNELS: list = [
        '-1001730438640', '-1001290638812', '-4003346612', '-1002037271958',
        '-1001872983219', '-1001760067536', '-1001887421284', '-1001800267709',
        '-1001739406499', '-1001895066412', '-1001561832074', '-1001780617105',
        '-1001862370670'
    ]
    
    # 关键词列表
    MONITOR_KEYWORDS: list = [
        '水滴', '水滴筹', 'shuidichou', 'shuidibao', '水滴保', '纵情向前',
        '互保', '翼帆', '深蓝保', 'WaterDrop', '大病', '筹款', '善款',
        '众筹', '保单', '短信', '劫持', '金融', '医院', '客户', '投保'
    ]
    
    # 数据库配置
    DB_HOST: str = '127.0.0.1'
    DB_PORT: int = 3306
    DB_USER: str = 'root'
    DB_PASSWORD: str = 'Secguard#2022'
    DB_NAME: str = 'threatnotice'
    
    # 飞书配置
    FEISHU_WEBHOOK_URL: str = 'https://open.feishu.cn/open-apis/bot/v2/hook/1e32e7d5-659e-4d26-aaa2-063a3e0cb941'
    
    class Config:
        env_file = '.env'

settings = Settings() 