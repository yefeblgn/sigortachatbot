from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    app_name: str = os.getenv("APP_NAME", "Sigorta Chatbot (Gemini)")
    version: str = os.getenv("APP_VERSION", "1.0.0")
    allow_origins: str = os.getenv("ALLOW_ORIGINS", "*")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    api_base: str = os.getenv("API_BASE", "http://localhost/api.php")

settings = Settings()
