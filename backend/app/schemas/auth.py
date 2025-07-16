from pydantic import BaseModel, EmailStr, model_validator
import re

class RegisterRequest(BaseModel):
    email: EmailStr
    password1: str
    password2: str
    nickname: str
    age: int
    gender: str

    @model_validator(mode="after")
    def validate_passwords(self):
        pw = self.password1

        if self.password1 != self.password2:
            raise ValueError("비밀번호가 일치하지 않습니다.")

        if not (8 <= len(pw) <= 30):
            raise ValueError("비밀번호는 최소 8자리 이상 또는 30자리 이하이어야 합니다.")
        if not re.search(r"[A-Za-z]", pw):
            raise ValueError("비밀번호에는 영문자가 포함되어야 합니다.")
        if not re.search(r"[0-9]", pw):
            raise ValueError("비밀번호에는 숫자가 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw):
            raise ValueError("비밀번호에는 특수문자가 포함되어야 합니다.")
        if re.search(r"(.)\1\1", pw):
            raise ValueError("같은 문자를 3번 이상 반복할 수 없습니다.")

        return self


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefreshRequest(BaseModel):
    refresh_token: str