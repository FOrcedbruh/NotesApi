from fastapi import APIRouter, Depends, Response, status
from .schemas import UserCreateSchema, UserSchema
from .helper import TokenInfo, create_refresh_token, create_access_token
from core import db_core
from sqlalchemy.ext.asyncio import AsyncSession
from . import actions




router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(actions.http_bearer)])


@router.post("/registration", response_model=TokenInfo)
async def registration(response: Response, user_in: UserCreateSchema, session: AsyncSession = Depends(db_core.session_creation)) -> TokenInfo:
    return await actions.registration(response=response, user_in=user_in, session=session)
    
    
    
    
@router.post("/login", response_model=TokenInfo)
async def login(response: Response, user_in: UserSchema = Depends(actions.validate_auth_user)):
    access_token = create_access_token(user=user_in)
    refresh_token = create_refresh_token(user=user_in)
    
    response.set_cookie(key="token", value=access_token)
    
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )
    



@router.post("/logout")
def logout(response: Response) -> dict:
    response.delete_cookie(key="token")
    
    return {
        "message": "Successfull logout",
        "status": status.HTTP_200_OK
    }


@router.get("/users/me")
def get_me(
        payload: dict = Depends(actions.get_current_token_payload),
        authUser: UserSchema = Depends(actions.get_current_auth_user)
    ) -> dict:
        return {
            "username": authUser.username,
            "email": authUser.email,
            "gender": authUser.gender
        }
        
    
# @router.post("/refresh", response_model=TokenInfo, response_model_exclude_none=True)
# def auth_refresh_jwt(user: UserSchema) -> TokenInfo:
#     access_token = create_access_token(user=user)
    
#     return TokenInfo(
#         access_token=access_token
#     )
    
