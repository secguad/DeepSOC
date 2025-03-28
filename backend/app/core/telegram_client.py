from telethon import TelegramClient, events
from telethon.tl.types import Message
from app.config.settings import settings

class TelegramMonitorClient:
    def __init__(self):
        self.client = TelegramClient(
            settings.TELEGRAM_PHONE,
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH
        )
        self.target_channels = settings.TELEGRAM_TARGET_CHANNELS
        self.keywords = settings.MONITOR_KEYWORDS

    async def start(self):
        """启动Telegram客户端"""
        await self.client.start()
        print("Telegram客户端已启动")

    async def stop(self):
        """停止Telegram客户端"""
        await self.client.disconnect()
        print("Telegram客户端已停止")

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