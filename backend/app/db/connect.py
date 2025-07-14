import asyncpg
from backend.app.core.config import settings

class AsyncDBPool:
    _pool: asyncpg.pool.Pool | None = None

    @classmethod
    async def init_pool(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                database=settings.POSTGRES_DB,
                host=settings.POSTGRES_HOST,
                port=int(settings.POSTGRES_PORT),
                min_size=1,
                max_size=10,
            )

    @classmethod
    async def close_pool(cls):
        if cls._pool:
            await cls._pool.close()

    @classmethod
    async def fetch_one(cls, sql: str, params: tuple = ()):
        async with cls._pool.acquire() as conn:
            return await conn.fetchrow(sql, *params)

    @classmethod
    async def fetch_all(cls, sql: str, params: tuple = ()):
        async with cls._pool.acquire() as conn:
            return await conn.fetch(sql, *params)

    @classmethod
    async def execute(cls, sql: str, params: tuple = ()):
        async with cls._pool.acquire() as conn:
            return await conn.execute(sql, *params)

    @classmethod
    async def execute_returning(cls, sql: str, params: tuple = ()):
        async with cls._pool.acquire() as conn:
            return await conn.fetchval(sql, *params)
