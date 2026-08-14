from pathlib import Path

from hknow.config.settings import Settings


def test_temp_data_dir_fixture(temp_data_dir: dict[str, Path]) -> None:
    """Verify that temporary data fixture creates accessible folders."""
    assert temp_data_dir["root"].exists()
    assert temp_data_dir["raw"].exists()
    assert temp_data_dir["processed"].exists()


def test_test_settings_fixture(
    test_settings: Settings, temp_data_dir: dict[str, Path]
) -> None:
    """Verify that the test settings fixture correctly binds isolated paths."""
    assert test_settings.app_env == "testing"
    assert test_settings.debug is True
    assert test_settings.log_level == "DEBUG"
    assert test_settings.raw_data_dir == temp_data_dir["raw"]
    assert test_settings.processed_data_dir == temp_data_dir["processed"]
