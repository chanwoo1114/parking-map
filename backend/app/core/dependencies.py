from fastapi import Header, HTTPException, Depends
from app.core.security import get_user_id_from_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-form")

async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    return user_id

# async def get_current_user_id(authorization: str = Header(...)):
#     if not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="잘못된 인증 형식입니다")
#
#     token = authorization.replace("Bearer ", "")
#     user_id = get_user_id_from_token(token)
#     if not user_id:
#         raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")
#     return user_id