from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List, Optional
import json
from app.core.dependencies import get_current_user_id
from app.schemas.parking import (
    ParkingLotUserAssignmentCreate, ResidentParkingLotUpdate,
    PublicParkingLotOut,
)
from app.db.queries.parking_queries import (
    insert_resident_parking_lot, update_resident_parking_lot,
    delete_resident_parking_lot, fetch_public_parking_lots
)

router = APIRouter(prefix="/parking-lots", tags=["ParkingLot"])

@router.post("", status_code=201)
async def create_parking_lot(
    payload: ParkingLotUserAssignmentCreate,
    user_id: int = Depends(get_current_user_id)
):
    data = payload.dict()

    parking_lot_id = await insert_resident_parking_lot((
        data['parking_lot_id'],
        user_id,
        data["total_spaces"],
        json.dumps(data.get("operating_hours")),
        json.dumps(data.get("price_policy"))
    ))

    if not parking_lot_id:
        raise HTTPException(status_code=500, detail="주차장 등록에 실패했습니다")

    return {"id": parking_lot_id, "message": "주차장이 등록되었습니다"}

@router.patch("/{parking_lot_id}", status_code=200)
async def update_parking_lot(
    parking_lot_id: int = Path(..., description="수정할 주차장 ID"),
    payload: ResidentParkingLotUpdate = ...,
    user_id: int = Depends(get_current_user_id)
):
    updates = payload.dict(exclude_none=True)

    if not updates:
        raise HTTPException(status_code=400, detail="수정할 데이터가 없습니다.")

    updated_id = await update_resident_parking_lot(parking_lot_id, user_id, updates)

    if not updated_id:
        raise HTTPException(status_code=404, detail="해당 주차장이 존재하지 않거나 수정 권한이 없습니다.")

    return {"id": updated_id, "message": "주차장 정보가 수정되었습니다"}

@router.delete("/{parking_lot_id}", status_code=200)
async def delete_parking_lot(
    parking_lot_id: int = Path(..., description="삭제할 주차장 ID"),
    user_id: int = Depends(get_current_user_id)
):
    deleted_id = await delete_resident_parking_lot(parking_lot_id, user_id)

    if not deleted_id:
        raise HTTPException(status_code=404, detail="해당 주차장을 찾을 수 없거나 삭제 권한이 없습니다.")

    return {"id": deleted_id, "message": "주차장이 비활성화되었습니다"}

@router.get("/summary", response_model=List[PublicParkingLotOut])
async def get_public_parking_lot(
    lng: float = Query(..., description="경도"),
    lat: float = Query(..., description="위도"),
    radius: int = Query(1500, description="반경(m)"),
):
    rows = await fetch_public_parking_lots(lng, lat, radius)

    return [PublicParkingLotOut(**r) for r in rows]