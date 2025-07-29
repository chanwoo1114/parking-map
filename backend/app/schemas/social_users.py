from pydantic import BaseModel, EmailStr
from typing import Optional

class SocialUserCreate(BaseModel):
    provider: str
    provider_id: str
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None


class SocialUserResponse(BaseModel):
    user_id: int
    provider: str
    provider_id: str
    email: Optional[EmailStr]
    nickname: Optional[str]

