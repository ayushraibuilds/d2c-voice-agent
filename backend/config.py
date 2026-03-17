"""
Centralized configuration for D2C Voice-First Agent.

Uses Pydantic BaseSettings for validated, type-safe config loaded from .env.
All secrets are loaded once at startup and accessed via the singleton `settings`.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # --- Twilio ---
    twilio_account_sid: str = Field(..., description="Twilio Account SID")
    twilio_auth_token: str = Field(..., description="Twilio Auth Token")

    # --- Groq ---
    groq_api_key: str = Field(..., description="Groq API key for LLM and Whisper")

    # --- LLM ---
    llm_model: str = Field(default="llama3-70b-8192", description="Groq LLM model name")
    llm_temperature: float = Field(default=0.0, description="LLM temperature")
    whisper_model: str = Field(default="whisper-large-v3", description="Groq Whisper model")
    vision_model: str = Field(default="llama-3.2-11b-vision-preview", description="Groq Vision LLM model name")

    # --- Observability & Tracking ---
    sentry_dsn: str | None = Field(default=None, description="Sentry DSN for error tracking")
    langchain_tracing_v2: str | None = Field(default=None, description="Enable LangSmith tracing (true/false)")
    langchain_project: str | None = Field(default=None, description="LangSmith project name")
    langchain_api_key: str | None = Field(default=None, description="LangSmith API Key")

    # --- Security ---
    validate_twilio_signature: bool = Field(
        default=True,
        description="Enable Twilio webhook signature validation (disable for local dev only)"
    )
    webhook_base_url: str = Field(
        default="http://localhost:8000",
        description="Public-facing base URL for Twilio signature validation (e.g. ngrok URL)"
    )

    # --- Database ---
    database_path: str = Field(
        default="d2c_agent.db",
        description="Path to SQLite database file (or connection string for PostgreSQL)"
    )

    # --- App ---
    app_version: str = Field(default="0.1.0")
    log_level: str = Field(default="INFO")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache()
def get_settings() -> Settings:
    """Return a cached singleton of the application settings."""
    return Settings()
