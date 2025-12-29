from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Database settings - using SQLite for development
    database_url: str = "sqlite:///./todo_app.db"

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