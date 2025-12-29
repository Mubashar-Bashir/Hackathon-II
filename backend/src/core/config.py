from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Database settings - using Neon PostgreSQL for Phase III
    neon_database_url: Optional[str] = None
    # Use neon_database_url if provided, otherwise default to local PostgreSQL
    database_url: str = "postgresql://user:pass@localhost:5432/todo_app"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # If neon_database_url is provided, use it as the primary database URL
        if self.neon_database_url:
            self.database_url = self.neon_database_url

    # Authentication settings
    better_auth_secret: str = "your-secret-key-here"
    jwt_expiration_hours: int = 24

    # Application settings
    app_name: str = "Todo App API"
    app_version: str = "0.1.0"
    debug: bool = True

    # CORS settings
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000,http://0.0.0.0:3000"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields in environment variables
    )


# Create a single instance of settings
settings = Settings()