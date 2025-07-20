from typing import Dict, Optional
from pydantic import BaseModel

class ParkingLotUserAssignmentCreate(BaseModel):
    parking_lot_id: int
    total_spaces: int
    operating_hours: Dict[str, str]
    price_policy: Dict[str, str]

class ResidentParkingLotUpdate(BaseModel):
    total_spaces: Optional[int] = None
    operating_hours: Optional[Dict[str, str]] = None
    price_policy: Optional[Dict[str, str]] = None