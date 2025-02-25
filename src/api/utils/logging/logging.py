"""Logger configuration."""

import logging
import os
import uuid
from sys import stderr
from typing import TYPE_CHECKING, Self

from colorama import Fore, Style
from loguru import logger
from properties import config

if TYPE_CHECKING:
    from loguru import Logger
else:
    Logger = logger


class LoggerConstructor:
    """
    Logger constructor class.

    Returns
    -------
    LoggerConstructor
        The logger constructor instance.
    """

    class InterceptHandler(logging.Handler):
        """
        Custom handler for intercepting standard logging messages.

        Parameters
        ----------
        logging : logging.Handler
            The logging handler to intercept.
        """

        def emit(self, record) -> None:
            """
            Emit a log record.

            Parameters
            ----------
            record : logging.LogRecord
                The log record to emit.
            """
            # Get corresponding Loguru level
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller to get correct stack depth
            frame, depth = logging.currentframe(), 2
            while (
                frame.f_back and frame.f_code.co_filename == logging.__file__
            ):
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Singleton instance
    _instance = None

    def __new__(cls) -> Self:
        """
        Create a new instance of the LoggerConstructor class.

        Returns
        -------
        Self
            The LoggerConstructor instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        # Remove existing handlers
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # Intercept standard logging
        logging.basicConfig(
            handlers=[self.InterceptHandler()],
            level=logging.DEBUG,
        )
        # Set logger instance to use and remove default handler
        self.logger = logger
        self.logger.remove(0)
        # Set log ID
        self.log_id = str(uuid.uuid4())[:8]

        # Add console handler
        self.logger.add(
            sink=stderr,
            level=config.logging.console.level,
            format=self.console_format,
        )

        console_remaining_space = os.get_terminal_size().columns - (
            len(config.logging.time_fmt)
            + config.logging.log_id_len
            + config.logging.level_len
            + config.logging.line_len
            + config.logging.name_len
            + config.logging.function_len
            + config.logging.message_len
            + config.logging.deduct_len
        )

        self.logger.console_format_category = (
            f"{Fore.GREEN}{'Time': <{len(config.logging.time_fmt) - 4}}{Style.RESET_ALL} | "
            f"{Fore.MAGENTA}{'Log ID': <{config.logging.log_id_len}}{Style.RESET_ALL} | "
            f"{Fore.WHITE}{'Level': <{config.logging.level_len}}{Style.RESET_ALL} | "
            f"{Fore.WHITE}{'Line': <{config.logging.line_len}}{Style.RESET_ALL} | "
            f"{Fore.CYAN}{'Name': <{config.logging.name_len}}{Style.RESET_ALL} | "
            f"{Fore.WHITE}{'Function': <{config.logging.function_len}}{Style.RESET_ALL} | "
            f"{Fore.WHITE}{'Message'}{Style.RESET_ALL}\n"
            f"{'─' * (len(config.logging.time_fmt) - 4 + 1)}┼"
            f"{'─' * (config.logging.log_id_len + 2)}┼"
            f"{'─' * (config.logging.level_len + 2)}┼"
            f"{'─' * (config.logging.line_len + 2)}┼"
            f"{'─' * (config.logging.name_len + 2)}┼"
            f"{'─' * (config.logging.function_len + 2)}┼"
            f"{'─' * console_remaining_space}\n"
        )

        if config.logging.console.show_categories:
            stderr.write(self.logger.console_format_category)

        # Add trace.log file handler
        log_file_type = "json" if config.logging.file.serialize else "log"
        for level in config.logging.file.levels:
            self.logger.add(
                sink=f"{config.logging.path + '/' + str(level).lower()}.{log_file_type}",
                level=level,
                format=self.file_format,
                serialize=config.logging.file.serialize,
                rotation=config.logging.file.rotation,
                retention=config.logging.file.retention,
                compression=config.logging.file.compression,
            )

    def console_format(self, record):
        _format = (
            f"<green>{{time:{config.logging.time_fmt}}}</green> "
            f"│ <magenta>{self.log_id: <{config.logging.log_id_len}}</magenta> "
            f"│ <level>{{level: <{config.logging.level_len}}}</level> "
            f"│ <level>{{line: <{config.logging.line_len}}}</level> "
            f"│ <level>{{name: <{config.logging.name_len}}}</level> "
            f"│ <level>{{function: <{config.logging.function_len}}}</level> "
            f"│ <level>{{message: <{config.logging.message_len}}}</level>"
        )

        if record["extra"]:
            # _format += " │ {extra}"
            _format += " │ <cyan>{extra}</cyan>"

        if record["exception"]:
            _format += "\n{exception}"
        else:
            _format += "\n"

        return _format

    def file_format(self, record):
        _format = (
            f"{{time:{config.logging.time_fmt}}} "
            f"│ {self.log_id: <{config.logging.log_id_len}} "
            f"│ {{level: <{config.logging.level_len}}} "
            f"│ {{line: <{config.logging.line_len}}} "
            f"│ {{name: <{config.logging.name_len}}} "
            f"│ {{function: <{config.logging.function_len}}} "
            f"│ {{message: <{config.logging.message_len}}}"
        )

        if record["extra"]:
            _format += " │ {extra}"

        if record["exception"]:
            _format += "\n{exception}"
        else:
            _format += "\n"

        return _format

    def get_logger(self) -> Logger:
        """
        Get the logger instance.

        Returns
        -------
        Logger
            The logger instance.
        """
        return self.logger
