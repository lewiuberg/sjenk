"""Model for booking."""

from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class BookedArea(Enum):
    """
    Types of booked area.

    Parameters
    ----------
    Enum : enum.Enum
        Base class for creating enumerated constants.
    """

    full = "full"
    half = "half"
    quarter = "quarter"


class Status(Enum):
    """
    Types of status.

    Parameters
    ----------
    Enum : enum.Enum
        Base class for creating enumerated constants.
    """

    active = "active"
    inactive = "inactive"
    cancelled = "cancelled"


class Booking(SQLModel, table=True):
    """
    Model for booking.

    Parameters
    ----------
    SQLModel : sqlmodel.SQLModel
        Base model for SQLModel.
    """

    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    place_id: int = Field(foreign_key="place.id")
    start_time: datetime
    end_time: datetime
    booked_area: BookedArea
    status: Status
