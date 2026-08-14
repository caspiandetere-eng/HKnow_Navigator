from pathlib import Path

from hknow.config.settings import Settings, get_settings


def test_default_settings():
    """Verify default configurations when no custom env is set."""
    settings = Settings()
    assert settings.app_name == "HKnow Navigator"
    assert settings.app_env in ["development", "testing", "production"]
    assert isinstance(settings.project_root, Path)


def test_directory_paths_resolution():
    """Verify raw and processed paths are resolved correctly relative to root."""
    settings = Settings()
    assert settings.raw_data_dir == settings.project_root / "data/raw"
    assert settings.processed_data_dir == settings.project_root / "data/processed"


def test_env_override(monkeypatch):
    """Verify that environment variables override defaults properly."""
    monkeypatch.setenv("APP_NAME", "HKnow Test Runner")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("APP_ENV", "testing")

    settings = Settings()
    assert settings.app_name == "HKnow Test Runner"
    assert settings.log_level == "DEBUG"
    assert settings.debug is True
    assert settings.app_env == "testing"


def test_get_settings_cached():
    """Verify get_settings returns a cached instance."""
    instance_1 = get_settings()
    instance_2 = get_settings()
    assert instance_1 is instance_2
