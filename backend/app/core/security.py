from passlib.context import CryptContext
from jose import jwt
from app.config import get_settings
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_token(token : str):
    return jwt.decode(
        token,
        # settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

