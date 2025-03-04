"""Model for place."""

from sqlmodel import Field, SQLModel


class Place(SQLModel, table=True):
    """
    Model for place.

    Parameters
    ----------
    SQLModel : sqlmodel.SQLModel
        Base model for SQLModel.
    """

    id: int = Field(primary_key=True, index=True)
    name: str = Field(max_length=50, unique=True)
    allow_partial_booking: bool
