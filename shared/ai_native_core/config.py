from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class AIConfig(BaseSettings):
    """
    Global configuration for AI Native projects.
    Loads from .env file automatically.
    """
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Tracing
    ENABLE_TRACING: bool = False
    otlp_endpoint: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = AIConfig()
