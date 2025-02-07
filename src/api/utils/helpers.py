"""Helper functions."""

from datetime import UTC, datetime


def seconds_elapsed(start_time: datetime, decimal_places: int = 2) -> str:
    """Get the number of seconds elapsed since the start time.

    Parameters
    ----------
    start_time : datetime
        The point in time to compare to.
    decimal_places : int, optional
        The number of decimal places to round to, by default 2.

    Returns
    -------
    str
        The number of seconds elapsed since the start time.
    """
    return str(
        round((datetime.now(UTC) - start_time).total_seconds(), decimal_places)
    )
