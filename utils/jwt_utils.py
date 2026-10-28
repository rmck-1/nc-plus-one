import os
from datetime import datetime, timedelta, timezone
import jwt

ALGORITHM = "HS256"

def get_secret():
    secret = os.getenv("JWT_SECRET")
    return secret

def create_access_token(id: int) -> str:
    payload = {
        "sub": str(id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=3)
    }
    return jwt.encode(payload, get_secret(), algorithm=ALGORITHM)