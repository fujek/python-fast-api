from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from auth.const import API_PATH_URL

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PATH_URL}/token")

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(username: str):
    to_encode = {"sub": username}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
