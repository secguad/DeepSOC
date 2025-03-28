import aiomysql
from datetime import datetime
from app.config.settings import settings
from app.models.keyword import Keyword

class KeywordService:
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

    async def create_keyword(self, keyword: Keyword) -> int:
        """
        创建新的关键词

        Args:
            keyword: Keyword对象

        Returns:
            int: 新创建的关键词ID
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = """
                INSERT INTO keywords (
                    word, category, risk_level, description,
                    created_by, created_at, updated_by, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
                values = (
                    keyword.word,
                    keyword.category,
                    keyword.risk_level,
                    keyword.description,
                    keyword.created_by,
                    datetime.now(),
                    keyword.updated_by,
                    datetime.now()
                )
                await cursor.execute(sql, values)
                return cursor.lastrowid

    async def update_keyword(self, keyword: Keyword) -> bool:
        """
        更新关键词信息

        Args:
            keyword: Keyword对象

        Returns:
            bool: 更新是否成功
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = """
                UPDATE keywords
                SET word = %s,
                    category = %s,
                    risk_level = %s,
                    description = %s,
                    updated_by = %s,
                    updated_at = %s
                WHERE id = %s
                """
                values = (
                    keyword.word,
                    keyword.category,
                    keyword.risk_level,
                    keyword.description,
                    keyword.updated_by,
                    datetime.now(),
                    keyword.id
                )
                await cursor.execute(sql, values)
                return cursor.rowcount > 0

    async def delete_keyword(self, keyword_id: int) -> bool:
        """
        删除关键词

        Args:
            keyword_id: 关键词ID

        Returns:
            bool: 删除是否成功
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = "DELETE FROM keywords WHERE id = %s"
                await cursor.execute(sql, (keyword_id,))
                return cursor.rowcount > 0

    async def get_keywords(
        self,
        category: str = None,
        risk_level: str = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[list[Keyword], int]:
        """
        获取关键词列表

        Args:
            category: 类别过滤
            risk_level: 风险等级过滤
            page: 页码
            page_size: 每页数量

        Returns:
            tuple: (关键词列表, 总数)
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                conditions = []
                values = []

                if category:
                    conditions.append("category = %s")
                    values.append(category)
                if risk_level:
                    conditions.append("risk_level = %s")
                    values.append(risk_level)

                where_clause = " AND ".join(conditions) if conditions else "1=1"
                offset = (page - 1) * page_size

                # 获取总数
                count_sql = f"SELECT COUNT(*) FROM keywords WHERE {where_clause}"
                await cursor.execute(count_sql, values)
                total = await cursor.fetchone()

                # 获取分页数据
                sql = f"""
                SELECT * FROM keywords
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """
                values.extend([page_size, offset])
                await cursor.execute(sql, values)
                rows = await cursor.fetchall()

                keywords = []
                for row in rows:
                    keyword = Keyword(
                        id=row[0],
                        word=row[1],
                        category=row[2],
                        risk_level=row[3],
                        description=row[4],
                        created_by=row[5],
                        created_at=row[6],
                        updated_by=row[7],
                        updated_at=row[8]
                    )
                    keywords.append(keyword)

                return keywords, total[0]

    async def get_keyword_by_id(self, keyword_id: int) -> Keyword:
        """
        根据ID获取关键词

        Args:
            keyword_id: 关键词ID

        Returns:
            Keyword: 关键词对象
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                sql = "SELECT * FROM keywords WHERE id = %s"
                await cursor.execute(sql, (keyword_id,))
                row = await cursor.fetchone()
                
                if row:
                    return Keyword(
                        id=row[0],
                        word=row[1],
                        category=row[2],
                        risk_level=row[3],
                        description=row[4],
                        created_by=row[5],
                        created_at=row[6],
                        updated_by=row[7],
                        updated_at=row[8]
                    )
                return None 