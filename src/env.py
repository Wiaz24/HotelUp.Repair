from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OAUTH2_CLIENT_ID: str
    OAUTH2_CLIENT_SECRET: str
    OAUTH2_METADATA_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()