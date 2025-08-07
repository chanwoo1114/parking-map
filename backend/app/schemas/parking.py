from typing import Dict, Optional, Union
from pydantic import BaseModel, field_validator
import json

class ParkingLotUserAssignmentCreate(BaseModel):
    parking_lot_id: int
    total_spaces: int
    operating_hours: Dict[str, str]
    price_policy: Dict[str, str]

class ResidentParkingLotUpdate(BaseModel):
    total_spaces: Optional[int] = None
    operating_hours: Optional[Dict[str, str]] = None
    price_policy: Optional[Dict[str, str]] = None

class PublicParkingLotOut(BaseModel):
    id: int
    lot_type: str
    geom: dict
    base_charge: str
    owner_id: Optional[int] = None
    is_available: Optional[bool] = None

    @field_validator('geom', mode='before')
    @classmethod
    def parse_geom(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v