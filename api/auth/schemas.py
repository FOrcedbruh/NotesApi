from pydantic import BaseModel, EmailStr, ConfigDict, Field




class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    
    id: int
    username: str
    password: str | bytes
    email: EmailStr | None
    gender: str


class UserCreateSchema(BaseModel):
    username: str
    password: str
    email: EmailStr | None
    gender: str
    
    
class UserLoginSchema(BaseModel):
    username: str
    password: str = Field(min_length=6)