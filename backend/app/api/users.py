from fastapi import APIRouter, HTTPException, Depends
from backend.app.core.dependencies import get_current_user_id
from backend.app.schemas.users import (
    UserInfoResponse, UpdateUserResponse,
    ChangePasswordRequest, DeleteAccountRequest
)
from backend.app.db.queries.user_queries import (
    get_user_info_by_id, update_user_info_by_id,
    get_password_hash_by_user_id, update_password_hash_by_user_id,
    deactivate_user_by_id
)
from backend.app.core.security import (
    hash_password, verify_password,
)

router = APIRouter(prefix="/users", tags=["Users"])

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