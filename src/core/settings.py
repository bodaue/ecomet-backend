from typing import Annotated

from pydantic import IPvAnyAddress, SecretStr, Field, BaseModel
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class PostgresSettings(BaseSettings, env_prefix="POSTGRES_"):
    host: IPvAnyAddress
    port: Annotated[int, Field(gt=0, lt=65536)]
    user: str
    password: SecretStr
    db: str

    def build_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.db}"
        )


class Settings(BaseModel):
    postgres: PostgresSettings


def create_settings() -> Settings:
    return Settings(postgres=PostgresSettings())
