import asyncio
import pandas as pd
import json
from app.db.queries.parking_queries import insert_parking_lot_base
from app.db.connect import AsyncDBPool

async def bulk_insert_parking_lots():
    with open('거주자우선주차구역.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data['records'])

    result = pd.DataFrame()
    result['external_id'] = df['거주자우선주차구획번호']
    result['name'] = df['거주자우선주차구역명']
    result['lot_type'] = 'resident'
    result['address'] = df['소재지지번주소']
    result['x'] = df['거주자우선주차구획경도'].astype(float)
    result['y'] = df['거주자우선주차구획위도'].astype(float)
    result['description'] = (
        "거주자우선주차구역명: " + df['거주자우선주차구역명'] +
        ", 주소: " + df['소재지지번주소']
    )

    records = result.to_dict(orient='records')

    await AsyncDBPool.init_pool()

    for row in records:
        try:
            await insert_parking_lot_base(row)
        except Exception as e:
            print(e)

    # 5. 커넥션 종료
    await AsyncDBPool.close_pool()


# 메인 실행
if __name__ == "__main__":
    asyncio.run(bulk_insert_parking_lots())
