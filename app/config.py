import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс Settings управляет конфигурацией приложения через переменные
    окружения. Настройки автоматически загружаются из `.env` или `.test.env`
    в зависимости от значения переменной `MODE`.
    """

    SECRET_KEY: str
    ALGORITHM: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    HOST: str
    PORT: int

    MODE: str = "DEV"

    @property
    def async_database_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=".test.env" if os.getenv("MODE") == "TEST" else ".env"
    )


settings = Settings()
