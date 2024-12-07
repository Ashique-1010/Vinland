from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

# Explicitly load the .env file
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()