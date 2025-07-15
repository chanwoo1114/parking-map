from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
from backend.app.core.dependencies import get_current_user_id
from backend.app.db.queries.user_queries import (
    get_user_info_by_id, update_user_info_by_id,
    get_password_hash_by_user_id, update_password_hash_by_user_id,
    deactivate_user_by_id
)
from backend.app.core.security import (
    hash_password, verify_password,
)
import re

router = APIRouter(prefix="/users", tags=["Users"])

class UserInfoResponse(BaseModel):
    email: EmailStr
    nickname: Optional[str]
    age: Optional[int]
    gender: Optional[str]


class UpdateUserResponse(BaseModel):
    nickname: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password1: str
    new_password2: str

    @model_validator(mode="after")
    def validate_all(self):
        if self.new_password1 != self.new_password2:
            raise ValueError("새 비밀번호가 일치하지 않습니다")
        if self.new_password1 == self.current_password:
            raise ValueError("동일한 비밀번호로는 변경이 불가능합니다")

        password = self.new_password1

        if not (8 <= len(password) <= 30):
            raise ValueError("비밀번호는 최소 8자리 이상 또는 30자리 이하이어야 합니다.")
        if not re.search(r"[A-Za-z]", password):
            raise ValueError("비밀번호에는 영문자가 포함되어야 합니다.")
        if not re.search(r"[0-9]", password):
            raise ValueError("비밀번호에는 숫자가 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("비밀번호에는 특수문자가 포함되어야 합니다.")
        if re.search(r"(.)\1\1", password):
            raise ValueError("같은 문자를 3번 이상 반복할 수 없습니다.")

        return self

class DeleteAccountRequest(BaseModel):
    password: str

@router.get("/me", response_model=UserInfoResponse)
async def get_my_info(user_id: int = Depends(get_current_user_id)):
    user = await get_user_info_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="사용자 정보를 찾을 수 없습니다")

    return dict(user)

@router.patch("/me", response_model=UpdateUserResponse)
async def update_my_info(
    payload: UpdateUserResponse,
    user_id: int = Depends(get_current_user_id)
):
    updated_user = update_user_info_by_id(
        user_id,
        nickname=payload.nickname,
        age=payload.age,
        gender=payload.gender
    )

    if not updated_user:
        raise HTTPException(status_code=400, detail="수정할 정보가 없습니다")

    return {"message": "정보가 성공적으로 수정되었습니다"}

@router.post("/change-password", response_model=ChangePasswordRequest)
async def change_password(
    payload: ChangePasswordRequest,
    user_id: int = Depends(get_current_user_id)
):
    current_hash = await get_password_hash_by_user_id(user_id)

    if not current_hash or not verify_password(payload.current_password, current_hash):
        raise HTTPException(status_code=400, detail="현재 비밀번호가 일치하지 않습니다.")

    new_hash = hash_password(payload.new_password1)
    await update_password_hash_by_user_id(user_id, new_hash)

    return {"message": "비밀번호가 성공적으로 변경되었습니다."}

@router.delete("/me", status_code=204)
async def deactivate_my_account(
    payload: DeleteAccountRequest,
    user_id: int = Depends(get_current_user_id)
):
    stored_hash = await get_password_hash_by_user_id(user_id)
    if not verify_password(payload.password, stored_hash):
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다")

    await deactivate_user_by_id(user_id)
    return