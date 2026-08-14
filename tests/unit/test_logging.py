import logging

from hknow.config.logging import get_logger, setup_logging


def test_get_logger():
    """Verify logger factory creates properly named logger instances."""
    logger = get_logger("hknow.test_module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "hknow.test_module"


def test_setup_logging_level():
    """Verify setup_logging configures root logger level properly."""
    setup_logging(log_level="DEBUG")
    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG

    setup_logging(log_level="WARNING")
    assert root_logger.level == logging.WARNING


def test_log_output(caplog):
    """Verify log output message and level propagation."""
    setup_logging(log_level="INFO")
    logger = get_logger("test_emitter")

    with caplog.at_level(logging.INFO):
        logger.info("Test logging message")

    assert "Test logging message" in caplog.text
    assert any(
        record.levelname == "INFO" and record.name == "test_emitter"
        for record in caplog.records
    )
