from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    APP_NAME: str = "eSports Championship API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Segurity
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "cualquiera-256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/base_de_datos"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000


settings = Settings()
