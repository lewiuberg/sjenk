"""Logging configuration."""

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
    Singleton class for creating and configuring the logger instance.

    Returns
    -------
    _instance : LoggerConstructor
        The LoggerConstructor instance
    """

    # Singleton instance
    __instance: Self = None

    def __new__(cls) -> Self:
        """
        Create a new instance of the LoggerConstructor class.

        Returns
        -------
        Self
            The LoggerConstructor instance
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._initialize()
        return cls.__instance

    def get_logger(self) -> Logger:
        """
        Get the logger instance.

        Returns
        -------
        Logger
            The logger instance.
        """
        return self._logger

    def _initialize(self) -> None:
        """Initialize the LoggerConstructor instance."""
        # Remove existing handlers
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # Map custom levels to standard logging levels
        level = self._map_log_level(config.logging.console.level)
        logging.basicConfig(
            handlers=[self.InterceptHandler()],
            level=level,
        )
        # Get all loggers from the logging module
        loggers = [
            logging.getLogger(name) for name in logging.root.manager.loggerDict
        ]

        # Intercept every logger
        for logger_name in loggers:
            logging_logger = logging.getLogger(logger_name.name)
            logging_logger.handlers = [self.InterceptHandler()]
            logging_logger.propagate = False
            logging_logger.setLevel(level)
        # Set logger instance to use and remove default handler
        self._logger = logger
        self._logger.remove(0)
        # Set log ID
        self._log_id = str(uuid.uuid4())[:8]

        # Add console handler
        self._logger.add(
            sink=stderr,
            level=level,
            format=self._console_format,
        )
        # Set console format category
        self.__set_console_format_category()

        # Add trace.log file handler
        log_file_type = "json" if config.logging.file.serialize else "log"
        for level in config.logging.file.levels:
            self._logger.add(
                sink=(
                    f"{config.logging.path + '/' + str(level).lower()}.{
                        log_file_type
                    }"
                ),
                level=level,
                format=self._file_format,
                serialize=config.logging.file.serialize,
                rotation=config.logging.file.rotation,
                retention=config.logging.file.retention,
                compression=config.logging.file.compression,
            )

    def _map_log_level(self, level: str) -> int:
        """
        Map custom log levels to standard logging levels.

        Parameters
        ----------
        level : str
            The custom log level to map

        Returns
        -------
        int
            The mapped log level
        """
        level_mapping = {
            "TRACE": logging.NOTSET,
            "NOTSET": logging.NOTSET,
            # Add other custom levels if needed
        }
        return level_mapping.get(level, logging.getLevelName(level))

    def _console_format(self, record: dict) -> str:
        """
        Format the log record for the console handler.

        Parameters
        ----------
        record : dict
            The log record to format

        Returns
        -------
        str
            The formatted log record
        """
        _format = (
            f"<green>{{time:{config.logging.time_fmt}}}</green> "
            f"│ <magenta>{self._log_id: <{config.logging.log_id_len}}</magenta> "  # noqa: E501
            f"│ <level>{{level: <{config.logging.level_len}}}</level> "
            f"│ <level>{{line: <{config.logging.line_len}}}</level> "
            f"│ <level>{{name: <{config.logging.name_len}}}</level> "
            f"│ <level>{{function: <{config.logging.function_len}}}</level> "
            f"│ <level>{{message: <{config.logging.message_len}}}</level>"
        )

        if record["extra"]:
            _format += " │ <cyan>{extra}</cyan>"

        if record["exception"]:
            _format += "\n{exception}"
        else:
            _format += "\n"

        return _format

    def _file_format(self, record: dict) -> str:
        """
        Format the log record for the file handler.

        Parameters
        ----------
        record : dict
            The log record to format

        Returns
        -------
        str
            The formatted log record
        """
        _format = (
            f"{{time:{config.logging.time_fmt}}} "
            f"│ {self._log_id: <{config.logging.log_id_len}} "
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

    def __set_console_format_category(self):
        """Set the console format category."""
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

        self._logger.console_format_category = (
            f"{Fore.GREEN}{'Time': <{len(config.logging.time_fmt) - 4}}{Style.RESET_ALL} | "  # noqa: E501
            f"{Fore.MAGENTA}{'Log ID': <{config.logging.log_id_len}}{Style.RESET_ALL} | "  # noqa: E501
            f"{Fore.WHITE}{'Level': <{config.logging.level_len}}{Style.RESET_ALL} | "  # noqa: E501
            f"{Fore.WHITE}{'Line': <{config.logging.line_len}}{Style.RESET_ALL} | "  # noqa: E501
            f"{Fore.CYAN}{'Name': <{config.logging.name_len}}{Style.RESET_ALL} | "  # noqa: E501
            f"{Fore.WHITE}{'Function': <{config.logging.function_len}}{Style.RESET_ALL} | "  # noqa: E501
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
            stderr.write(self._logger.console_format_category)

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

            # Add logger name to the record
            logger_name = record.name

            # Prepend log message with logger name
            logger.opt(depth=depth, exception=record.exc_info).log(
                level, f"[{logger_name}] {record.getMessage()}"
            )
