from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from auth.const import API_PATH_URL
from auth.schema import User, TokenUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PATH_URL}/token")

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user: User):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_user = TokenUser(sub=user.username, user_id=user.id, exp=expire, role=user.role)
    encoded_jwt = jwt.encode(token_user.dict(), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str = Depends(oauth2_scheme)) -> TokenUser:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenUser.model_validate(payload)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
