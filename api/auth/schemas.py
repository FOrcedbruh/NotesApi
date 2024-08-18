from pydantic import BaseModel, EmailStr, ConfigDict



class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    
    id: int
    username: str
    password: str | bytes
    fullname: str
    email: EmailStr | None