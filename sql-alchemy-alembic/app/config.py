from pydantic_settings import BaseSettings, SettingsConfigDict
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseSettings):
    db_url: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env")
    )

settings = Settings()