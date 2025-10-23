"""
Application settings and configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # LLM Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    llm_provider: str = "openai"  # openai or anthropic
    llm_model: str = "gpt-4o"
    temperature: float = 0.7

    # Application
    app_name: str = "ESM Chatbot"
    session_secret_key: str = "change-me-in-production"

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Chainlit Settings
    chainlit_host: str = "0.0.0.0"
    chainlit_port: int = 8080

    # Experiment Configuration
    experiment_config_path: str = "config/experiments.yaml"

    # Data Export
    export_dir: str = "exports"

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()


# Create exports directory if it doesn't exist
settings = get_settings()
os.makedirs(settings.export_dir, exist_ok=True)
