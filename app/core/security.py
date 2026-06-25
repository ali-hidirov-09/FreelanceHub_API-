from datetime import datetime, timedelta, timezone
from jose import JWSError, jwt
from typing import Optional
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password,hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt