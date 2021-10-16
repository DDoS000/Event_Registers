import jwt
from jwt import PyJWTError
from pydantic import ValidationError
from datetime import datetime, timedelta
from utils import constantUtil as const
from auth import service, schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

async def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, const.SECRET_KEY, algorithm=const.ALGORITHM_HS256)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login",
)

def get_token_user(token: str = Depends(oauth2_scheme)):
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, const.SECRET_KEY, algorithms=[const.ALGORITHM_HS256])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        # Check blacklist token
        black_list_token = await service.find_blacklist_token(token)
        if black_list_token:
            raise credentials_exception

        # Check user existed
        result = await service.find_exist_user(username)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        return schema.UserResponse(**result)

    except (PyJWTError, ValidationError):
        raise credentials_exception


def get_current_active_user(current_user: schema.UserResponse = Depends(get_current_user)):
    if current_user.status != '1':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")

    return current_user