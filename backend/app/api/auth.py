from fastapi import APIRouter, HTTPException, Query
from app.schemas.auth import (
    RegisterRequest, LoginRequest,
    TokenResponse, TokenRefreshRequest
)
from app.core.security import (
    hash_password, verify_password,
    create_refresh_token, create_access_token,
    get_user_id_from_token,
)
from app.db.queries.user_queries import (
    is_email_taken, get_user_email_query,
    is_nickname_taken, create_email_user,
    create_email_user
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

'''회원 가입'''
@router.post("/register", status_code=201)
async def register_user(payload: RegisterRequest):
    print(payload)
    if await is_email_taken(payload.email):
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다")

    try:
        user_id = await create_email_user(payload)

    except Exception as e:
        raise HTTPException(status_code=500, detail="사용자 생성 중 오류가 발생했습니다")

    return {"message": "회원가입 완료", "user_id": user_id}

'''이메일 중복 체크'''
@router.get("/check-email")
async def check_email_duplicate(email: str = Query(...)):
    is_dup = await is_email_taken(email)
    return {"is_duplicate": bool(is_dup)}

'''닉네임 중복 체크'''
@router.get("/check-nickname")
async def check_nickname_duplicate(nickname: str = Query(...)):
    is_dup = await is_nickname_taken(nickname)
    return {"is_duplicate": bool(is_dup)}


'''로그인'''
@router.post("/login", response_model=TokenResponse)
async def login_user(payload: LoginRequest):
    user_info = await get_user_email_query(payload.email)

    if not user_info:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다.")

    user_id, hashed_pw, is_active = user_info

    if not is_active:
        raise HTTPException(status_code=403, detail="비활성화된 계정입니다. 관리자에게 문의하세요.")

    if not verify_password(payload.password, hashed_pw):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다.")

    access_token = create_access_token({"user_id": user_id})
    refresh_token = create_refresh_token({"user_id": user_id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )

'''토큰 갱신'''
@router.post('refresh', response_model=TokenResponse)
async def refresh_token(payload: TokenRefreshRequest):
    try:
        user_id = get_user_id_from_token(payload.refresh_token)

    except HTTPException as e:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    new_access_token = create_access_token({"user_id": user_id})
    new_refresh_token = create_refresh_token({"user_id": user_id})

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )

