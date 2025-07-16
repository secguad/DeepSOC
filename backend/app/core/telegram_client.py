import asyncio
import logging
from telethon import TelegramClient, events
from telethon.tl.types import Channel, User
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.crud import monitor as monitor_crud
from app.models.monitor import MonitorChannel, ChannelStatus
from app.services.content_analyzer import ContentAnalyzer
from app.core.config import settings

logger = logging.getLogger(__name__)

class TelegramMonitorClient:
    def __init__(self):
        self.client = None
        self.is_running = False
        self.monitored_channels = {}
        self.db = None
        self.content_analyzer = None

    async def init_client(self, db: Session):
        """初始化Telegram客户端"""
        self.db = db
        self.client = TelegramClient(
            'monitor_session',
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH
        )
        await self.client.start()
        
        # 初始化内容分析器
        self.content_analyzer = ContentAnalyzer(db)

    async def start_monitoring(self):
        """开始监控"""
        if self.is_running:
            return
        
        self.is_running = True
        logger.info("开始Telegram消息监控")
        
        # 获取所有活跃的Telegram频道
        channels = monitor_crud.get_channels(self.db)
        for channel in channels:
            if channel.status == ChannelStatus.ACTIVE:
                await self._monitor_channel(channel)

    async def stop_monitoring(self):
        """停止监控"""
        if not self.is_running:
            return
        
        self.is_running = False
        logger.info("停止Telegram消息监控")
        
        # 取消所有监控任务
        for channel_id in self.monitored_channels:
            self.monitored_channels[channel_id].cancel()
        self.monitored_channels.clear()

    async def _monitor_channel(self, channel: MonitorChannel):
        """监控单个频道"""
        try:
            # 获取频道实体
            channel_entity = await self.client.get_entity(channel.name)
            
            # 创建消息处理器
            @self.client.on(events.NewMessage(chats=channel_entity))
            async def handle_new_message(event):
                if not self.is_running:
                    return
                
                try:
                    # 获取消息内容
                    message = event.message
                    content = message.text if message.text else ""
                    
                    # 分析消息内容
                    analysis = await self.content_analyzer.analyze_content(content)
                    
                    # 如果可信度大于阈值且AI确认包含敏感信息，保存消息
                    if (analysis["score"] >= settings.MONITOR_RELIABILITY_THRESHOLD and 
                        analysis["is_sensitive"]):
                        
                        # 保存消息
                        await self._save_message(
                            channel_id=channel.id,
                            source=f"Telegram-{channel.name}",
                            content=content,
                            url=f"https://t.me/c/{channel_entity.id}/{message.id}",
                            reliability=analysis["reliability"],
                            sensitive_type=analysis["sensitive_type"],
                            ai_explanation=analysis["ai_explanation"]
                        )
                        
                        # 更新频道最后更新时间
                        channel.last_update = datetime.utcnow()
                        self.db.commit()
                        
                        logger.info(f"发现敏感信息: {content[:100]}...")
                        logger.info(f"AI分析结果: {analysis['ai_explanation']}")
                
                except Exception as e:
                    logger.error(f"处理消息时出错: {str(e)}")
            
            # 记录监控任务
            self.monitored_channels[channel.id] = handle_new_message
            
        except Exception as e:
            logger.error(f"监控频道 {channel.name} 时出错: {str(e)}")

    async def _save_message(
        self,
        channel_id: int,
        source: str,
        content: str,
        url: Optional[str] = None,
        reliability: str = "低",
        sensitive_type: str = "未知",
        ai_explanation: str = ""
    ):
        """保存消息到数据库"""
        message_data = {
            "channel_id": channel_id,
            "time": datetime.utcnow(),
            "source": source,
            "content": content,
            "reliability": reliability,
            "url": url,
            "sensitive_type": sensitive_type,
            "ai_explanation": ai_explanation
        }
        
        monitor_crud.create_message(self.db, message_data)

    async def get_chat_info(self, chat_id: int) -> dict:
        """获取聊天信息"""
        try:
            chat = await self.client.get_entity(chat_id)
            return {
                'id': chat.id,
                'title': chat.title,
                'type': 'channel' if hasattr(chat, 'broadcast') else 'group'
            }
        except Exception as e:
            print(f"获取聊天信息失败: {e}")
            return None

    async def download_media(self, message: Message, file_path: str) -> str:
        """下载媒体文件"""
        try:
            return await self.client.download_media(message, file_path)
        except Exception as e:
            print(f"下载媒体文件失败: {e}")
            return None

    def is_target_channel(self, chat_id: str) -> bool:
        """检查是否是目标频道"""
        return str(chat_id) in self.target_channels

    def contains_keywords(self, text: str) -> list:
        """检查文本是否包含关键词"""
        found_keywords = []
        for keyword in self.keywords:
            if keyword.lower() in text.lower():
                found_keywords.append(keyword)
        return found_keywords

    def add_message_handler(self, handler):
        """添加消息处理器"""
        self.client.add_event_handler(handler, events.NewMessage) 