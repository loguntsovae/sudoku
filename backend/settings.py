from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    SECRET_KEY: str = config("SECRET_KEY", default="your_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()