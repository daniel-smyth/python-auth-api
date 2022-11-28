import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Pydantic base settings

    Info: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    environment: str = os.getenv("environment")
    """Environment: dev/production"""

    APP_URL: str = os.getenv("APP")
    """Front end URL"""
    APP_URL_DEV: str = os.getenv("APP_DEV")
    """Front end URL"""

    DB_URL: str = os.getenv("DB_URL")
    """MongoDB connection URL"""
    DB_NAME: str = os.getenv("DB_NAME")
    """MongoDB database name"""
    DB_NAME_DEV: str = os.getenv("DB_NAME_DEV")
    """MongoDB database name"""

    AWS_KEY: str = os.getenv("AWS_KEY")
    """AWS connection key"""
    AWS_SECRET: str = os.getenv("AWS_SECRET")
    """AWS connection secret key"""

    secret_key: str = os.getenv("secret_key")
    """JWT secret key"""
    algorithm: str = "HS256"
    """JWT algorithm"""

    class Config:
        env_file = ".env"
        orm_mode = True


@lru_cache
def get_settings():
    """
    Least-recently-used cache for application settings
    """

    return Settings()
