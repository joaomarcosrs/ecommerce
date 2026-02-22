from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from jwt import decode, encode
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from ecommerce.core.settings import settings

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
pwd_context = PasswordHash.recommended()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        payload=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password=password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(
        password=plain_password,
        hash=hashed_password,
    )


def get_token_subject(token: str) -> str:
    try:
        payload = decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        subject = payload.get('sub')
        if not subject:
            raise HTTPException(
                status_code=401,
                detail='Could not validate credentials.',
            )
        return subject
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail='Could not validate credentials.',
        )
