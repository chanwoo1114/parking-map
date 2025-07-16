from fastapi import APIRouter, Depends, HTTPException
from backend.app.core.dependencies import get_current_user_id
from backend.app.schemas.parking import (
    ParkingLotCreateRequest,
)
from backend.app.db.queries.parking_queries import (
    insert_parking_lot
)

router = APIRouter(prefix="/parking-lots", tags=["ParkingLot"])

@router.post("", status_code=201)
async def create_parking_lot(
    payload: ParkingLotCreateRequest,
    user_id: int = Depends(get_current_user_id)
):
    data = payload.dict()
    data["owner_id"] = user_id

    parking_lot_id = await insert_parking_lot(data)
    if not parking_lot_id:
        raise HTTPException(status_code=500, detail="주차장 등록에 실패했습니다")

    return {"id": parking_lot_id, "message": "주차장이 등록되었습니다"}
