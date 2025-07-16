from pydantic import BaseModel, Field
from typing import Optional

class ParkingLotCreateRequest(BaseModel):
    name: str
    lot_type: str
    address: Optional[str]
    latitude: float
    longitude: float
    total_spaces: int
    available_spaces: int
    operating_hours: Optional[dict] = Field(default_factory=dict)
    price_policy: Optional[dict] = Field(default_factory=dict)
    description: Optional[str]
    external_id: Optional[str]