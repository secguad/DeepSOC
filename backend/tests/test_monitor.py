import pytest
import asyncio
from datetime import datetime
from app.core.telegram_client import TelegramMonitorClient
from app.services.content_analyzer import ContentAnalyzer
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.monitor import MonitorChannel, MonitorMessage
from app.crud import monitor as monitor_crud

@pytest.mark.asyncio
async def test_telegram_monitor():
    """测试Telegram消息监听功能"""
    # 初始化数据库会话
    db = SessionLocal()
    
    # 创建测试频道
    test_channel = MonitorChannel(
        channel_id="test_channel",
        channel_name="测试频道",
        channel_type="telegram",
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(test_channel)
    db.commit()
    
    # 初始化Telegram客户端
    client = TelegramMonitorClient()
    
    # 初始化内容分析器
    content_analyzer = ContentAnalyzer(db)
    
    try:
        # 启动监听
        await client.start_monitoring()
        
        # 等待一段时间以接收消息
        await asyncio.sleep(10)
        
        # 检查是否有消息被保存
        messages = monitor_crud.get_messages(db, channel_id=test_channel.channel_id)
        assert len(messages) > 0
        
        # 检查消息内容分析
        for message in messages:
            # 分析消息内容
            analysis_result = await content_analyzer.analyze_content(
                message.content,
                message.file_url if message.file_url else None
            )
            
            # 验证分析结果
            assert analysis_result["reliability"] in ["高", "中", "低"]
            assert "keywords" in analysis_result
            assert "score" in analysis_result
            assert "is_sensitive" in analysis_result
            
            # 打印分析结果
            print(f"\n消息分析结果:")
            print(f"可信度: {analysis_result['reliability']}")
            print(f"匹配关键词: {[k['keyword'] for k in analysis_result['keywords']]}")
            print(f"可信度分数: {analysis_result['score']}")
            print(f"是否包含敏感信息: {analysis_result['is_sensitive']}")
            if analysis_result.get("sensitive_type"):
                print(f"敏感信息类型: {analysis_result['sensitive_type']}")
            if analysis_result.get("data_scale"):
                print(f"数据规模: {analysis_result['data_scale']}")
            if analysis_result.get("data_fields"):
                print(f"数据字段: {analysis_result['data_fields']}")
            if analysis_result.get("ai_explanation"):
                print(f"AI分析说明: {analysis_result['ai_explanation']}")
            
    finally:
        # 停止监听
        await client.stop_monitoring()
        
        # 清理测试数据
        db.delete(test_channel)
        db.commit()
        db.close()

@pytest.mark.asyncio
async def test_content_analysis():
    """测试内容分析功能"""
    # 初始化数据库会话
    db = SessionLocal()
    
    # 初始化内容分析器
    content_analyzer = ContentAnalyzer(db)
    
    # 测试不同类型的消息
    test_messages = [
        {
            "content": "保险混合样本.xlsx 包含1000条用户数据",
            "file_url": None
        },
        {
            "content": "泄露的客户信息，包含手机号和身份证号",
            "file_url": "https://example.com/files/customer_data.xlsx"
        },
        {
            "content": "内部文档泄露，包含源代码和业务数据",
            "file_url": "https://example.com/files/internal_doc.zip"
        }
    ]
    
    try:
        for message in test_messages:
            # 分析消息内容
            result = await content_analyzer.analyze_content(
                message["content"],
                message["file_url"]
            )
            
            # 验证分析结果
            assert result["reliability"] in ["高", "中", "低"]
            assert "keywords" in result
            assert "score" in result
            assert "is_sensitive" in result
            
            # 打印分析结果
            print(f"\n消息内容: {message['content']}")
            print(f"可信度: {result['reliability']}")
            print(f"匹配关键词: {[k['keyword'] for k in result['keywords']]}")
            print(f"可信度分数: {result['score']}")
            print(f"是否包含敏感信息: {result['is_sensitive']}")
            if result.get("sensitive_type"):
                print(f"敏感信息类型: {result['sensitive_type']}")
            if result.get("data_scale"):
                print(f"数据规模: {result['data_scale']}")
            if result.get("data_fields"):
                print(f"数据字段: {result['data_fields']}")
            if result.get("ai_explanation"):
                print(f"AI分析说明: {result['ai_explanation']}")
            
    finally:
        db.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 