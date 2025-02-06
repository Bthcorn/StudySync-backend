from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self
from pydantic import computed_field, PostgresDsn
from pydantic_core import MultiHostUrl


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"

    DB_HOST: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int = 5432

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str


settings = Setting()
