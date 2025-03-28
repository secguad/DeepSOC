import requests
from app.config.settings import settings

class FeishuClient:
    def __init__(self):
        self.webhook_url = settings.FEISHU_WEBHOOK_URL

    def send_message(self, content: str) -> bool:
        """
        向飞书机器人发送消息

        Args:
            content: 要发送的消息内容

        Returns:
            bool: 发送是否成功
        """
        try:
            message = {
                "msg_type": "text",
                "content": {
                    "text": content
                }
            }

            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                self.webhook_url,
                json=message,
                headers=headers,
                timeout=5
            )

            if response.status_code == 200:
                print("飞书消息发送成功")
                return True
            else:
                print(f"飞书消息发送失败，状态码：{response.status_code}")
                print(f"错误信息：{response.text}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"发送飞书消息时发生异常：{e}")
            return False

    def format_alert_message(self, alert_data: dict) -> str:
        """
        格式化告警消息

        Args:
            alert_data: 告警数据字典

        Returns:
            str: 格式化后的消息内容
        """
        return (
            f"关键词监听：{', '.join(alert_data['keywords'])}\n"
            f"频道ID：{alert_data['channel_id']}\n"
            f"频道名称：{alert_data['channel_name']}\n"
            f"消息：{alert_data['content']}\n"
            f"消息日期：{alert_data['date']}"
        ) 