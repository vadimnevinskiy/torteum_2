from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_async_url(self) -> str:
        return (f"postgresql+asyncpg://"
                f"{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}"
                f"/{self.DB_NAME}")

    @property
    def database_sync_url(self) -> str:
        return (f"postgresql+psycopg://"
                f"{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}"
                f"/{self.DB_NAME}")


settings = Settings()
