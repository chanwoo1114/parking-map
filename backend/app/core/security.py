from passlib.context import CryptContext
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(pain_password, hashed_password):
    return pwd_context.verify(pain_password, hashed_password)

