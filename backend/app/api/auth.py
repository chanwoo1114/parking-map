from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from backend.app.core.security import (
    hash_password, verify_password,
    create_refresh_token, create_access_token
)
from backend.app.db.queries.user_queries import (
    select_user_email_query, insert_app_user_query,
    insert_email_user_query, get_user_email_query
)
import re

router = APIRouter(prefix="/auth", tags=["Auth"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password1: str
    password2: str
    nickname: str
    age: int
    gender: str

    @field_validator("password1")
    def validate_password(cls, password):
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

        return password

    @field_validator('password2')
    def passwords_match(cls, v, info):
        password1 = info.data.get("password1")
        if password1 is None:
            return v

        if password1 != v:
            raise ValueError("비밀번호가 일치하지 않습니다")

        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register", status_code=201)
def register_user(payload: RegisterRequest):
    if select_user_email_query(payload.email):
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다")

    user_id = insert_app_user_query()
    if not user_id:
        raise HTTPException(status_code=500, detail="사용자 생성 실패")

    hashed_pw = hash_password(payload.password1)

    insert_email_user_query((
        user_id, payload.email, hashed_pw,
        payload.nickname, payload.age, payload.gender
    ))

    return {"message": "회원가입 완료"}

@router.post("/login", response_model=TokenResponse)
def login_user(payload: LoginRequest):
    user_info = get_user_email_query(payload.email)

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

