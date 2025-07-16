from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
import re

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
