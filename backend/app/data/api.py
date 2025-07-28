import asyncio
import requests
from backend.app.core.security import settings
from backend.app.db.queries.parking_queries import insert_parking_lot_base
from backend.app.db.connect import AsyncDBPool

async def parking_info_api():
    http = "http://apis.data.go.kr/B553881/Parking/PrkSttusInfo?"
    service_key = settings.API_KEY
    number_of_rows = '10'
    format = '2'
    page_no = 2602

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
