from typing import Annotated

from pydantic import SecretStr, Field, BaseModel
from pydantic_settings import BaseSettings as _BaseSettings, SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class GithubSettings(BaseSettings, env_prefix="GITHUB_"):
    access_token: SecretStr


class PostgresSettings(BaseSettings, env_prefix="POSTGRES_"):
    host: str
    port: Annotated[int, Field(gt=0, lt=65536)]
    user: str
    password: SecretStr
    db: str

    def build_dsn(self) -> str:
        return (
            f"postgresql://"
            f"{self.user}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.db}"
        )


class ParserSettings(BaseModel):
    github: GithubSettings
    postgres: PostgresSettings


def create_parser_settings() -> ParserSettings:
    return ParserSettings(github=GithubSettings(), postgres=PostgresSettings())
