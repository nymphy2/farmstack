from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from jose import jwt
from passlib.context import CryptContext

from core.config import settings
from core.google_verify import validate_google_token


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

ALGORITHM = 'HS256'

reusable_oauth2 = HTTPBearer(scheme_name='Authorization')


def create_access_token(
    subject: Union[Any, str], expires_delta: timedelta = None
) -> str:
    """Create access_token when user signin.

    Args:
        subject (Union[Any, str]): user info to be encoded in token.
        expires_delta (timedelta, optional): token expire time delta. Defaults to None.

    Returns:
        str: token generated by jwt.
    """
    if expires_delta:
        expire_time = datetime.now() + expires_delta
    else:
        expire_time = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {'exp': expire_time, 'sub': str(subject)}
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)
    return encode_jwt


def validate_token(
    http_authorization_credentials=Depends(reusable_oauth2)
) -> str:
    """Decode token

    Args:
        http_authorization_credentials: Authorization info from headers.

    Raises:
        HTTPException: if token is wrong or expired.

    Returns:
        str: token payload.
    """
    token = http_authorization_credentials.credentials
    try:
        if (
            len(token) > 500
        ):
            payload = validate_google_token(token)
        else:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[ALGORITHM]
            )
        return payload
    except(jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail='Invalid credentials')


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hashing_password(password: str) -> str:
    return pwd_context.hash(password)
