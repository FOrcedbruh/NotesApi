from fastapi import APIRouter, Depends, HTTPException, status, Form
from .schemas import UserSchema
from .helper import create_access_token, create_refresh_token, TokenInfo




from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials


http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")



router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(http_bearer)])


@router.post("/login", response_model=TokenInfo)
def login(user: UserSchema ) -> TokenInfo:
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )
    
