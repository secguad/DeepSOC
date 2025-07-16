import logging
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud import keyword as keyword_crud
from app.models.keyword import Keyword
from app.core.config import settings
from app.services.file_analyzer import FileAnalyzer
import openai
import re

logger = logging.getLogger(__name__)

class ContentAnalyzer:
    def __init__(self, db: Session):
        self.db = db
        self.keywords = []
        self.load_keywords()
        self.file_analyzer = FileAnalyzer()
        
        # 初始化OpenAI客户端
        openai.api_key = settings.OPENAI_API_KEY
        
        # 可信度评分规则
        self.reliability_rules = {
            "高": {
                "min_score": 0.8,
                "weight": 1.0,
                "patterns": [
                    # 文件名模式
                    r"[\w\s]+(?:用户|客户|会员|数据|信息|样本|名单|资料)[\w\s]*\.(?:xlsx|xls|csv|txt)",
                    r"[\w\s]+(?:用户|客户|会员|数据|信息|样本|名单|资料)[\w\s]*\.(?:rar|zip|7z)",
                    # 内容描述模式
                    r"包含[\d,]+条(?:用户|客户|会员|数据|信息|样本|名单|资料)",
                    r"[\d,]+条(?:用户|客户|会员|数据|信息|样本|名单|资料)泄露",
                    # 数据特征
                    r"(?:手机号|电话|身份证|邮箱|地址|姓名|账号|密码)",
                    r"(?:用户ID|客户ID|会员ID|订单号|交易号)",
                ]
            },
            "中": {
                "min_score": 0.6,
                "weight": 0.7,
                "patterns": [
                    # 文件名模式
                    r"[\w\s]+(?:数据|信息|资料)[\w\s]*\.(?:xlsx|xls|csv|txt)",
                    # 内容描述模式
                    r"包含(?:用户|客户|会员|数据|信息|样本|名单|资料)",
                    # 数据特征
                    r"(?:性别|年龄|职业|收入|地区)",
                ]
            },
            "低": {
                "min_score": 0.4,
                "weight": 0.4,
                "patterns": [
                    # 文件名模式
                    r"[\w\s]+\.(?:xlsx|xls|csv|txt)",
                    # 内容描述模式
                    r"(?:数据|信息|资料)",
                ]
            }
        }

    def load_keywords(self):
        """加载关键词列表"""
        try:
            self.keywords = keyword_crud.get_keywords(self.db)
        except Exception as e:
            logger.error(f"加载关键词失败: {str(e)}")
            self.keywords = []

    def calculate_reliability_score(self, content: str, matched_keywords: List[Dict], file_analysis: Optional[Dict] = None) -> float:
        """计算可信度分数"""
        score = 0.0
        total_weight = 0.0
        
        # 1. 根据关键词风险等级计算基础分数
        for keyword in matched_keywords:
            weight = self.reliability_rules[keyword["risk_level"]]["weight"]
            score += weight
            total_weight += weight
        
        # 2. 根据内容特征调整分数
        for level, rules in self.reliability_rules.items():
            for pattern in rules["patterns"]:
                if re.search(pattern, content, re.IGNORECASE):
                    score += rules["weight"] * 0.3
        
        # 3. 根据文件大小调整分数（如果包含）
        if re.search(r"[\d.]+[MB|GB]", content, re.IGNORECASE):
            score += 0.2
        
        # 4. 根据数据量调整分数
        data_count_match = re.search(r"(\d+)[条|个|份]", content)
        if data_count_match:
            count = int(data_count_match.group(1))
            if count >= 10000:
                score += 0.3
            elif count >= 1000:
                score += 0.2
            elif count >= 100:
                score += 0.1
        
        # 5. 如果文件分析成功，根据文件内容调整分数
        if file_analysis and file_analysis.get("success"):
            file_results = file_analysis.get("results", [])
            for result in file_results:
                # 检查列名是否包含敏感信息
                columns = result.get("columns", [])
                for column in columns:
                    if any(pattern in column for pattern in ["手机", "电话", "身份证", "邮箱", "地址", "姓名", "账号", "密码"]):
                        score += 0.3
                    elif any(pattern in column for pattern in ["性别", "年龄", "职业", "收入", "地区"]):
                        score += 0.2
                
                # 检查内容是否包含敏感信息
                content = result.get("content", "")
                if any(pattern in content for pattern in ["手机号", "电话", "身份证", "邮箱", "地址", "姓名", "账号", "密码"]):
                    score += 0.3
                elif any(pattern in content for pattern in ["性别", "年龄", "职业", "收入", "地区"]):
                    score += 0.2
        
        # 6. 归一化分数
        if total_weight > 0:
            score = min(1.0, score / total_weight)
        
        return score

    def get_reliability_level(self, score: float) -> str:
        """根据分数确定可信度等级"""
        if score >= self.reliability_rules["高"]["min_score"]:
            return "高"
        elif score >= self.reliability_rules["中"]["min_score"]:
            return "中"
        else:
            return "低"

    async def analyze_with_ai(self, content: str, matched_keywords: List[Dict], file_analysis: Optional[Dict] = None) -> Dict:
        """使用AI分析内容可信度"""
        try:
            # 构建提示词
            prompt = f"""请分析以下内容是否包含用户数据泄露，并给出可信度评估（0-1分）和详细说明。
内容：{content}
匹配到的关键词：{', '.join([k['keyword'] for k in matched_keywords])}

文件分析结果：
{file_analysis if file_analysis else '无文件分析结果'}

请按以下格式回复：
可信度分数：0.8
可信度说明：详细说明为什么给出这个分数
是否包含敏感信息：是/否
敏感信息类型：用户数据/客户数据/会员数据/交易数据
数据规模：具体数量（如：1000条用户数据）
数据字段：包含的字段（如：姓名、手机号、身份证号等）
"""

            # 调用OpenAI API
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一个专业的数据安全分析师，负责评估用户数据泄露的可信度。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # 解析AI响应
            ai_response = response.choices[0].message.content
            score_match = re.search(r"可信度分数：(\d+\.?\d*)", ai_response)
            explanation_match = re.search(r"可信度说明：(.+?)(?=\n|$)", ai_response)
            sensitive_match = re.search(r"是否包含敏感信息：(.+?)(?=\n|$)", ai_response)
            type_match = re.search(r"敏感信息类型：(.+?)(?=\n|$)", ai_response)
            scale_match = re.search(r"数据规模：(.+?)(?=\n|$)", ai_response)
            fields_match = re.search(r"数据字段：(.+?)(?=\n|$)", ai_response)
            
            return {
                "ai_score": float(score_match.group(1)) if score_match else 0.0,
                "ai_explanation": explanation_match.group(1) if explanation_match else "",
                "is_sensitive": sensitive_match.group(1) == "是" if sensitive_match else False,
                "sensitive_type": type_match.group(1) if type_match else "未知",
                "data_scale": scale_match.group(1) if scale_match else "未知",
                "data_fields": fields_match.group(1) if fields_match else "未知"
            }
            
        except Exception as e:
            logger.error(f"AI分析失败: {str(e)}")
            return {
                "ai_score": 0.0,
                "ai_explanation": "AI分析失败",
                "is_sensitive": False,
                "sensitive_type": "未知",
                "data_scale": "未知",
                "data_fields": "未知"
            }

    async def analyze_content(self, content: str, file_url: Optional[str] = None) -> Dict:
        """分析内容"""
        try:
            # 匹配关键词
            matched_keywords = []
            for keyword in self.keywords:
                if keyword.keyword.lower() in content.lower():
                    matched_keywords.append({
                        "keyword": keyword.keyword,
                        "category": keyword.category,
                        "risk_level": keyword.risk_level
                    })
            
            if not matched_keywords:
                return {
                    "reliability": "低",
                    "keywords": [],
                    "score": 0.0,
                    "is_sensitive": False
                }
            
            # 如果有文件URL，分析文件内容
            file_analysis = None
            if file_url:
                file_analysis = await self.file_analyzer.analyze_file(file_url)
            
            # 计算基础可信度分数
            base_score = self.calculate_reliability_score(content, matched_keywords, file_analysis)
            
            # 使用AI进行二次分析
            ai_analysis = await self.analyze_with_ai(content, matched_keywords, file_analysis)
            
            # 综合评分
            final_score = (base_score + ai_analysis["ai_score"]) / 2
            
            return {
                "reliability": self.get_reliability_level(final_score),
                "keywords": matched_keywords,
                "score": final_score,
                "is_sensitive": ai_analysis["is_sensitive"],
                "sensitive_type": ai_analysis["sensitive_type"],
                "data_scale": ai_analysis["data_scale"],
                "data_fields": ai_analysis["data_fields"],
                "ai_explanation": ai_analysis["ai_explanation"],
                "file_analysis": file_analysis
            }
            
        except Exception as e:
            logger.error(f"内容分析失败: {str(e)}")
            return {
                "reliability": "低",
                "keywords": [],
                "score": 0.0,
                "is_sensitive": False,
                "sensitive_type": "未知",
                "data_scale": "未知",
                "data_fields": "未知",
                "ai_explanation": "分析失败",
                "file_analysis": None
            } 