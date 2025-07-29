import asyncio
import requests
import asyncpg
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    SECRET_KEY: str
    API_KEY: str

    KAKAO_CLIENT_ID: str
    KAKAO_CLIENT_SECRET: str
    KAKAO_REDIRECT_URI: str

    NAVER_CLIENT_ID: str
    NAVER_CLIENT_SECRET: str
    NAVER_REDIRECT_URI: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    class Config:
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        env_file_encoding = "utf-8"

settings = Settings()

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

async def insert_parking_lot_base(data: dict):
    sql = """
            INSERT INTO public.parking_lot_base (external_id, name, lot_type, address, geom, description)
            SELECT $1, $2, $3, $4, ST_SetSRID(ST_MakePoint($5, $6), 4326), $7 
            WHERE NOT EXISTS (
            SELECT 1 FROM public.parking_lot_base
            WHERE external_id = $1::VARCHAR AND name = $2::VARCHAR
            )
            RETURNING id;
            """
    return await AsyncDBPool.execute_returning(sql, (
        data.get("external_id"),
        data["name"],
        data["lot_type"],
        data.get("address"),
        data["x"],
        data["y"],
        data["description"]
    ))

async def parking_info_api():
    http = "http://apis.data.go.kr/B553881/Parking/PrkSttusInfo?"
    service_key = 'lchYOllVvCEhzpzVzmc1T4rOcFMQePdGt8BUaHRzJHEL6P8ZcHtZwBIF0q6h%2BJbJ2Xm9cIZjYnMoGi5CMc0TyQ%3D%3D'
    number_of_rows = '10'
    format = '2'
    page_no = 3355

    await AsyncDBPool.init_pool()

    while True:
        try:
            url = (
                f"{http}serviceKey={service_key}"
                f"&pageNo={page_no}&numOfRows={number_of_rows}&format={format}"
            )
            response = requests.get(url)
            datas = response.json()

            data = datas.get('PrkSttusInfo')
            if not data:
                break

            for i in data:
                await insert_parking_lot_base({
                    'external_id': i['prk_center_id'],
                    'name': i['prk_plce_nm'],
                    'lot_type': 'public',
                    'address': i['prk_plce_adres'],
                    'x': float(i['prk_plce_entrc_lo']) if i.get('prk_plce_entrc_lo') else None,
                    'y': float(i['prk_plce_entrc_la']) if i.get('prk_plce_entrc_la') else None,
                    'description': f"주차구역명: {i['prk_plce_nm']}, 주소: {i['prk_plce_adres']}"
                })
            print(data)
            print(page_no)

            page_no += 1

        except Exception as e:
            print(f"Error on page {page_no}: {e}")
            breakpoint()

    await AsyncDBPool.close_pool()

if __name__ == "__main__":
    asyncio.run(parking_info_api())
