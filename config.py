from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    db_url: str
    db_name: str
    bot_token: str

    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache
def get_config():
    return Config()



