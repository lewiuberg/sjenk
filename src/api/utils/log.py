"""Utility function for returning the same logger object."""

import os
import uuid
from sys import stdout
from typing import TYPE_CHECKING

import setuptools.dist  # noqa: F401
import stackprinter
from loguru import logger

if TYPE_CHECKING:
    from loguru import Logger
else:
    Logger = logger

from notifiers.logging import NotificationHandler


def get_logger(
    colorize: bool = True,
    serialize: bool = False,
    rotation: str = "1 days",
    retention: str = "30 days",
    compression: str = "zip",
    slack_webhook: str = "",
) -> Logger:
    """Get the logger object.

    Parameters
    ----------
    colorize : bool, optional
        Colorize the console output, by default True
    serialize : bool, optional
        Serialize the console output, by default False
    rotation : str, optional
        The amount of time before making a new log file, by default "1 days"
    retention : str, optional
        The amount of time before deleting old log files, by default "30 days"
    compression : str, optional
        The compression algorithm to use for old log files, by default "zip"
    console_format : Callable, optional
        The format for console output, by default console_format
    file_format : Callable, optional
        The format for file output, by default file_format
    slack_format : Callable, optional
        The format for slack output, by default slack_format
    slack_webhook : str, optional
        The slack webhook url, by default SLACK_WEBHOOK

    Returns
    -------
    Logger
        The logger object

    Examples
    --------
    >>> from utils import get_logger
    >>> logger = get_logger()
    >>> logger.trace("A trace message.")
    >>> logger.debug("A debug message.")
    >>> logger.info("An info message.")
    >>> logger.success("A success message.")
    >>> logger.warning("A warning message.")
    >>> logger.error("An error message.")
    >>> logger.critical("A critical message.")
    """
    logs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
    )
    logger.remove()

    log_id = str(uuid.uuid4())[:8]

    def console_format(record) -> str:
        """Format the console output according to the log level.

        Parameters
        ----------
        record : dict
            The log record.

        Returns
        -------
        str
            The formatted log record.
        """
        format_ = (
            "<green>{time:YYYY-MM-DD_HH:mm:ss}</green> "
            "| <level>{level: <8}</level> "
            f"| <magenta>{log_id: <8}</magenta> "
            "| <cyan>{name: <34}</cyan> "
            "| <level>{function: <26}</level> "
            "| <level>{line: <4}</level> "
            "| <level>{message}</level>"
        )

        if record["level"].no >= 40:
            record["extra"]["stack"] = stackprinter.format(record["exception"])
            format_ += "\n{extra[stack]}\n"
        else:
            format_ += "\n"

        return format_

    def file_format(record) -> str:
        """Format the file output.

        Parameters
        ----------
        record : dict
            The log record.

        Returns
        -------
        str
            The formatted log record.
        """
        return (
            "{time:YYYY-MM-DD_HH:mm:ss} "
            "| {level: <8} "
            f"| {log_id: <8} "
            "| {name: <16} "
            "| {function: <16} "
            "| {line: <4} "
            "| {message}\n"
        )

    def slack_format(record) -> str:
        """Format the slack output.

        Parameters
        ----------
        record : dict
            The log record.

        Returns
        -------
        str
            The formatted log record.
        """
        return (
            "{time:YYYY-MM-DD_HH:mm:ss} "
            "| {level:} "
            f"| {log_id:} "
            "| {name:} "
            "| {function:} "
            "| {line:} "
            "| {message}\n"
        )

    logger.add(
        sink=stdout,
        level="TRACE",
        format=console_format,
        colorize=colorize,
    )

    logger.add(
        sink=f"{logs_path}/trace.log",
        level="TRACE",
        format=file_format,
        colorize=colorize,
        serialize=serialize,
        rotation=rotation,
        retention=retention,
        compression=compression,
    )

    logger.add(
        sink=f"{logs_path}/error.log",
        level="ERROR",
        format=file_format,
        colorize=colorize,
        serialize=serialize,
        rotation=rotation,
        retention=retention,
        compression=compression,
    )

    # logger.add(
    #     NotificationHandler(
    #         "slack",
    #         defaults={
    #             "webhook_url": slack_webhook,
    #         },
    #     ),
    #     level="ERROR",
    #     format=slack_format,
    # )

    logger.add(
        NotificationHandler(
            "email",
            defaults={
                "subject": "Sjenk Critical Error",
                "to": "some@email.com",
                "from": "some@email.com",
                "host": "smtp.prod.local",
                "port": 25,
                "login": False,
            },
        ),
        level="CRITICAL",
        format=file_format,
    )

    return logger
