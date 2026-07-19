from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RapidAid AI"
    environment: str = "development"
    frontend_origin: str = "http://localhost:5173"

    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    supabase_bucket: str = "injury-scans"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"

    whatsapp_access_token: str | None = None
    whatsapp_phone_number_id: str | None = None
    default_emergency_contact: str | None = None

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.frontend_origin.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
