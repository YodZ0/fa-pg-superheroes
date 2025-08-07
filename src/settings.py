from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent  # fa-pg-superheroes


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000


class APIConfig(BaseModel):
    prefix: str = "/api"


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str
    provider: str = "postgresql+asyncpg"

    @property
    def dsn(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class SuperHeroApiConfig(BaseModel):
    access_token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_file=(BASE_DIR / ".env"),
        extra="ignore",
    )
    base_dir: Path = BASE_DIR
    debug: bool
    cors_origins: list[str] = ["*"]
    run: RunConfig = RunConfig()
    api: APIConfig = APIConfig()
    db: DatabaseConfig
    sh_api: SuperHeroApiConfig


settings = Settings()