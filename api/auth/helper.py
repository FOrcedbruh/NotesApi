from .schemas import UserSchema
from .utils import encode_jwt, decode_jwt
from pydantic import BaseModel
from core.config import authSettings


TOKEN_TYPE_KEY = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"



def create_token(data: dict, token_type: str, expire_minutes: int = authSettings.expire_of_access_token_minutes, ) -> str:
    payload = {TOKEN_TYPE_KEY: token_type}
    payload.update(data)
    return encode_jwt(payload=payload, expire_minutes=expire_minutes)



def create_access_token(user: UserSchema) -> str:
    payload = {
        "sub": user.username,
        "email": user.email,
    }
    return create_token(data=payload, token_type=ACCESS_TOKEN_TYPE, expire_minutes=authSettings.expire_of_access_token_minutes)
def create_refresh_token(user: UserSchema) -> str:
    payload = {
        "sub": user.username
    }
    return create_token(data=payload, token_type=REFRESH_TOKEN_TYPE, expire_minutes=authSettings.expire_of_refresh_token_minutes)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    
    