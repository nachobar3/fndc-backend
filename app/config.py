from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    MONGO_URI: str  
    RESEND_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GOOGLE_CLIENT_ID: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 