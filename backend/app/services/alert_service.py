import aiomysql
from datetime import datetime
from app.config.settings import settings
from app.models.alert import Alert

class AlertService:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        """初始化数据库连接池"""
        self.pool = await aiomysql.create_pool(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB_NAME,
            autocommit=True
        )

    async def close_pool(self):
        """关闭数据库连接池"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def create_alert(self, alert: Alert) -> int:
        """
        创建新的告警记录

        Args:
            alert: Alert对象

        Returns:
            int: 新创建的告警ID
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = """
                INSERT INTO alerts (
                    title, content, link, type, src_site, date,
                    keywords, channel_id, channel_name, risk_level,
                    status, processed_by, processed_at, process_comment
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                """
                values = (
                    alert.title,
                    alert.content,
                    alert.link,
                    alert.type,
                    alert.src_site,
                    alert.date,
                    ','.join(alert.keywords),
                    alert.channel_id,
                    alert.channel_name,
                    alert.risk_level,
                    alert.status,
                    alert.processed_by,
                    alert.processed_at,
                    alert.process_comment
                )
                await cursor.execute(sql, values)
                return cursor.lastrowid

    async def update_alert_status(
        self,
        alert_id: int,
        status: str,
        processed_by: str,
        process_comment: str
    ) -> bool:
        """
        更新告警状态

        Args:
            alert_id: 告警ID
            status: 新状态
            processed_by: 处理人
            process_comment: 处理说明

        Returns:
            bool: 更新是否成功
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = """
                UPDATE alerts
                SET status = %s,
                    processed_by = %s,
                    processed_at = %s,
                    process_comment = %s
                WHERE id = %s
                """
                values = (
                    status,
                    processed_by,
                    datetime.now(),
                    process_comment,
                    alert_id
                )
                await cursor.execute(sql, values)
                return cursor.rowcount > 0

    async def get_alerts(
        self,
        status: str = None,
        risk_level: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[list[Alert], int]:
        """
        获取告警列表

        Args:
            status: 状态过滤
            risk_level: 风险等级过滤
            start_date: 开始日期
            end_date: 结束日期
            page: 页码
            page_size: 每页数量

        Returns:
            tuple: (告警列表, 总数)
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                conditions = []
                values = []

                if status:
                    conditions.append("status = %s")
                    values.append(status)
                if risk_level:
                    conditions.append("risk_level = %s")
                    values.append(risk_level)
                if start_date:
                    conditions.append("date >= %s")
                    values.append(start_date)
                if end_date:
                    conditions.append("date <= %s")
                    values.append(end_date)

                where_clause = " AND ".join(conditions) if conditions else "1=1"
                offset = (page - 1) * page_size

                # 获取总数
                count_sql = f"SELECT COUNT(*) FROM alerts WHERE {where_clause}"
                await cursor.execute(count_sql, values)
                total = await cursor.fetchone()

                # 获取分页数据
                sql = f"""
                SELECT * FROM alerts
                WHERE {where_clause}
                ORDER BY date DESC
                LIMIT %s OFFSET %s
                """
                values.extend([page_size, offset])
                await cursor.execute(sql, values)
                rows = await cursor.fetchall()

                alerts = []
                for row in rows:
                    alert = Alert(
                        id=row[0],
                        title=row[1],
                        content=row[2],
                        link=row[3],
                        type=row[4],
                        src_site=row[5],
                        date=row[6],
                        keywords=row[7].split(','),
                        channel_id=row[8],
                        channel_name=row[9],
                        risk_level=row[10],
                        status=row[11],
                        processed_by=row[12],
                        processed_at=row[13],
                        process_comment=row[14]
                    )
                    alerts.append(alert)

                return alerts, total[0] 