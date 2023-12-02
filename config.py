from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    TOKEN: SecretStr
    DADATA_API_KEY: SecretStr
    DADATA_SECRET_KEY: SecretStr
    DB_URI: SecretStr
    POSTGRES_PASSWORD: SecretStr
    ANTICAPTCHA_API_KEY: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
