from sqlalchemy import select
from core.models import User
from .helper import create_access_token, create_refresh_token, TokenInfo
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserLoginSchema, UserCreateSchema, UserSchema
from .utils import hash_password, decode_jwt, valid_password
from fastapi import HTTPException, status, Response, Depends, Form
from core import db_core
from core.models import User
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import InvalidTokenError




http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")



def get_current_token_payload(
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        token: str = Depends(oauth2_scheme)
    ):
        try:
            payload = decode_jwt(token=token)
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token error: {e}"
            )
        return payload



async def get_current_auth_user(payload: dict = Depends(get_current_token_payload), session: AsyncSession = Depends(db_core.session_creation)) -> UserSchema:
    username: str | None = payload.get("sub")
    
    st = await  session.execute(select(User).filter(User.username == username))
    user = st.scalars().first()
    
    
    if user:
        return user
    
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found"
    )
    
    
    
async def validate_auth_user(
    session: AsyncSession = Depends(db_core.session_creation),
    password: str = Form(),
    username: str = Form(),
):
    unauthexc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )
    st = await session.execute(select(User).filter(User.username == username))
    user = st.scalars().first()
    
    if not user:
        raise unauthexc
    
    if valid_password(
        password=password,
        hashed_password=user.password
    ):
        return user
    
    raise unauthexc
        
    
    

async def registration(response: Response, session: AsyncSession, user_in: UserCreateSchema) -> TokenInfo:
    st = await session.execute(select(User).filter(User.username == user_in.username))
    candidate = st.scalars().first()
    
    if candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exist"
        )
    else:
        hashedPass: bytes = hash_password(password=user_in.password)
        user_in.password = hashedPass
            
        user = User(**user_in.model_dump())
            
        session.add(user)
            
        await session.commit()
            
            
        access_token = create_access_token(user=user)
        refresh_token = create_refresh_token(user=user)
        
        response.set_cookie(key="access_token", value=access_token)
            
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token
        )
    



    


            
            
            