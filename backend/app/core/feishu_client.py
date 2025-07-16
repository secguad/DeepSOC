import requests
from app.core.config import settings

class FeishuClient:
    def __init__(self):
        self.webhook_url = settings.FEISHU_WEBHOOK

    def send_message(self, content: str) -> bool:
        """
        向飞书机器人发送消息

        Args:
            content: 要发送的消息内容

        Returns:
            bool: 发送是否成功
        """
        if not self.webhook_url:
            return False
            
        try:
            response = requests.post(
                self.webhook_url,
                json={
                    "msg_type": "text",
                    "content": {
                        "text": content
                    }
                }
            )
            return response.status_code == 200
        except Exception as e:
            print(f"发送飞书消息失败: {str(e)}")
            return False

    def format_alert_message(self, alert_data: dict) -> str:
        """
        格式化告警消息

        Args:
            alert_data: 告警数据字典

        Returns:
            str: 格式化后的消息内容
        """
        return f"""
告警信息：
时间：{alert_data.get('time', '')}
级别：{alert_data.get('level', '')}
类型：{alert_data.get('type', '')}
来源：{alert_data.get('source', '')}
内容：{alert_data.get('content', '')}
        """ 