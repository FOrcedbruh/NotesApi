import jwt
import bcrypt
from core.config import authSettings
import datetime


def encode_jwt(
    payload: dict,
    secret: str = authSettings.secret,
    algorithm: str =authSettings.algorithm,
    expire_minutes: int = authSettings.expire_of_access_token_minutes
):
    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.UTC)
    expire = now + datetime.timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(payload=payload, key=secret, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    secret: str = authSettings.secret,
    algoritm: str = authSettings.algorithm
):
    decoded = jwt.decode(jwt=token, key=secret, algorithms=[algoritm])
    return decoded


def hash_password(
    password: str | bytes
) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password=password.encode(), salt=salt)


def valid_password(
    hashed_password: bytes,
    password: str
) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)