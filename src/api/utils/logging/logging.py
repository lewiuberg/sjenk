"""Logger configuration."""

import logging
import uuid
from sys import stderr

from loguru import logger
from properties import config  # noqa: F401


class LoggerConstructor:
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller to get correct stack depth
            frame, depth = logging.currentframe(), 2
            while frame.f_back and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Remove existing handlers
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Intercept standard logging
        logging.basicConfig(handlers=[self.InterceptHandler()], level=logging.INFO)

        self.log_id = str(uuid.uuid4())[:8]

        self._console_format = (
            "<green>{time:YYYY-MM-DD_HH:mm:ss}</green> "
            "| <level>{level: <8}</level> "
            f"| <magenta>{self.log_id: <8}</magenta> "
            "| <cyan>{name: <34}</cyan> "
            "| <level>{function: <26}</level> "
            "| <level>{line: <4}</level> "
            "| <level>{message}</level>"
        )

        self.logger = logger
        self.logger.remove(0)
        self.logger.add(
            stderr,
            level="TRACE",
            # format="<green>{time}</green> | {level} | {message} | {extra}",
            format=self._console_format,
            filter="",
            colorize=True,
            backtrace=True,
            diagnose=True,
        )

    def get_logger(self):
        return self.logger
