from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME: str = os.environ.get("DB_NAME")
DB_USER: str = os.environ.get("DB_USER")
DB_PASS: str = os.environ.get("DB_PASS")
DB_HOST: str = os.environ.get("DB_HOST")
DB_PORT: str = os.environ.get("DB_PORT")
JWT_SECRET: str = os.environ.get("JWT_SECRET")

class Settings(BaseSettings):
    db_url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    db_echo: bool = True
    
    
class AuthSettings(BaseModel):
    secret: str = JWT_SECRET
    algorithm: str =  "HS256"
    expire_of_access_token_minutes: int = 20
    expire_of_refresh_token_minutes: int = 60 * 24 * 30
    
    
    
authSettings = AuthSettings()
    

settings = Settings()