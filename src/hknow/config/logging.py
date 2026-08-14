"""
Centralized logging configuration for HKnow.
Provides structured log formatting and log-level propagation.
"""

import logging
import sys

from hknow.config.settings import get_settings

# Standard structured log format
DEFAULT_LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
)
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(
    log_level: str | None = None,
    log_format: str = DEFAULT_LOG_FORMAT,
    date_format: str = DEFAULT_DATE_FORMAT,
) -> None:
    """
    Configures the root logger.

    Parameters
    ----------
    log_level : Optional[str]
        Explicit log level string (e.g., 'DEBUG', 'INFO').
        If None, falls back to `Settings.log_level`.
    log_format : str
        Format string for log records.
    date_format : str
        Format string for timestamps.
    """
    if log_level is None:
        settings = get_settings()
        log_level = settings.log_level

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Avoid adding duplicate handlers if setup_logging is called multiple times
    if not root_logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    else:
        for handler in root_logger.handlers:
            handler.setLevel(numeric_level)


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Factory function to retrieve a configured logger instance.

    Parameters
    ----------
    name : Optional[str]
        Module or component name (usually __name__).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    return logging.getLogger(name or "hknow")
