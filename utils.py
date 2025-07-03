from datetime import datetime, timedelta
from jose import jwt
from .config import settings

def create_download_token(user_id: int, file_id: int, expires_minutes: int = 15):
    payload = {
        "sub": str(user_id),
        "file_id": file_id,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_download_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
