from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./cookly.db"
    secret_key: str = "dev-only-change-me-dev-only-change-me"
    access_token_minutes: int = 15
    refresh_token_days: int = 30
    openai_api_key: str = ""
    openai_model_light: str = "gpt-4o-mini"
    openai_model_strong: str = "gpt-4o"
    cors_origins: str = "http://localhost:5173"
    media_dir: str = "./media"
    login_max_attempts: int = 5
    login_window_minutes: int = 15


settings = Settings()
