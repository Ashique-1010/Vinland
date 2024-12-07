from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer 
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.core.security import verify_token
from app.services.auth import get_user_by_email
from app.config import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "api/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"recieved token: {token}")
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credential",
        headers = {"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = verify_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user
                    