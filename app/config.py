# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_hostname: str = Field(..., env='DATABASE_HOSTNAME')
    database_port: str = Field(..., env='DATABASE_PORT')
    database_password: str = Field(..., env='DATABASE_PASSWORD')
    database_username: str = Field(..., env='DATABASE_USERNAME')
    database_name: str = Field(..., env='DATABASE_NAME')
    secret_key: str = Field(..., env='SECRET_KEY')
    algorithm: str = Field(..., env='ALGORITHM')
    access_token_expire_minutes: int = Field(..., env='ACCESS_TOKEN_EXPIRE_MINUTES')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', case_sensitive=False)

settings = Settings()

# Uncomment the following line for debugging
# print(settings.dict())m pydantic_settings import BaseSettings
