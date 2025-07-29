from datetime import timedelta, datetime
from http.client import HTTPException
from passlib.context import CryptContext
from app.core.config import settings
import jwt
from jwt.exceptions import InvalidTokenError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(pain_password, hashed_password):
    return pwd_context.verify(pain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None

def get_user_id_from_token(token: str):
    payload = decode_token(token)

    if not payload or "user_id" not in payload:
        raise HTTPException(401, deatil="유효하지 않은 토큰입니다.")

    return payload["user_id"]