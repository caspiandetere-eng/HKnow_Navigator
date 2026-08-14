"""
Configuration management for HKnow.
Loads and validates settings from environment variables and .env files.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings model.
    Reads values from environment variables or a .env file.
    """

    # Application metadata
    app_name: str = Field(
        default="HKnow Navigator", description="Name of the application"
    )
    app_env: Literal["development", "testing", "production"] = Field(
        default="development", description="Operating environment mode"
    )
    debug: bool = Field(default=False, description="Debug mode toggle")

    # Central Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Global log level"
    )

    # Base Paths
    # Points to the repository root directory (2 levels up from src/hknow/config/)
    project_root: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent
    )

    # Data Directories (Relative to project_root by default)
    data_raw_dir_name: str = Field(
        default="data/raw", description="Subpath for raw ingested files"
    )
    data_processed_dir_name: str = Field(
        default="data/processed", description="Subpath for cleaned/chunked data"
    )

    @property
    def raw_data_dir(self) -> Path:
        """Returns the absolute Path to the raw data directory."""
        path = self.project_root / self.data_raw_dir_name
        return path

    @property
    def processed_data_dir(self) -> Path:
        """Returns the absolute Path to the processed data directory."""
        path = self.project_root / self.data_processed_dir_name
        return path

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Factory function providing a cached singleton instance of Settings.
    """
    return Settings()
