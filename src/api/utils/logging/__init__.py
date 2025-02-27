"""Initializes the logger instance for the API."""

from utils.logging.logging import LoggerConstructor

logger_instance = LoggerConstructor()
logger = logger_instance.get_logger()
