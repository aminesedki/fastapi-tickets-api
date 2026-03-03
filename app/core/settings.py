from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Docker compose values automatically override defaults.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Base path
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # App config
    APP_TITLE: str = "TICKETS API"
    APP_VERSION: str = "1.0.0"

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080

    ENV: str = "dev"

    API_VERSION: str = "v1"

    # Database
    DB_NAME: str = "app.db"

    DATABASE_URL: str | None = None  # allow override

    @property
    def is_prod(self) -> bool:
        return self.ENV.lower() == "prod"
    
    @property
    def DB_PATH(self) -> Path:
        return self.BASE_DIR / self.DB_NAME

    @property
    def LOG_DIR(self) -> Path:
        path = self.BASE_DIR / "logs"
        path.mkdir(parents=True, exist_ok=True)  # auto-create logs dir
        return path

    @property
    def LOG_FILE_PATH(self) -> Path:
        return self.LOG_DIR / "app.log"

    @property
    def computed_database_url(self) -> str:
        """
        if DATABASE_URL is provided (Docker compose)
        else Otherwise build SQLite path automatically
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"sqlite+aiosqlite:///{self.DB_PATH}"

    @property
    def API_BASE_PREFIX(self) -> str:
        return f"/api/{self.API_VERSION}"
    


settings = Settings()
