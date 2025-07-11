from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class DBSettings(BaseModel):
    driver: str = "sqlite"
    host: str | None = None
    port: int | None = None
    name: str | None = "./test.db"
    user: str | None = None
    password: str | None = None

class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=['.env.prod', '.env.local', '.env'], env_nested_delimiter="_", extra="ignore")
    
    db: DBSettings = DBSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
