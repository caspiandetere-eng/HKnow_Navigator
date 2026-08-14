"""
Central pytest configuration and shared fixtures for HKnow test suites.
"""

from collections.abc import Generator
from pathlib import Path

import pytest

from hknow.config.settings import Settings, get_settings


@pytest.fixture
def temp_data_dir(tmp_path: Path) -> dict[str, Path]:
    """
    Creates an isolated temporary data folder structure for test isolation.
    """
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    return {
        "root": tmp_path,
        "raw": raw_dir,
        "processed": processed_dir,
    }


@pytest.fixture
def test_settings(
    temp_data_dir: dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> Generator[Settings, None, None]:
    """
    Provides a configured Settings instance isolated to temporary paths.
    Clears cache before and after test execution.
    """
    get_settings.cache_clear()

    # Override environment paths to point to the temporary directories
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = Settings(
        project_root=temp_data_dir["root"],
        data_raw_dir_name="raw",
        data_processed_dir_name="processed",
    )

    yield settings

    get_settings.cache_clear()
