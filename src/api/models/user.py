"""Model for user."""

from enum import Enum

from sqlmodel import Field, SQLModel


class UserRole(Enum):
    """
    Types of user roles.

    Parameters
    ----------
    Enum : enum.Enum
        User role names.
    """

    admin = "admin"
    leader = "leader"
    member = "member"
    user = "user"


class User(SQLModel, table=True):
    """
    Model for user.

    Parameters
    ----------
    SQLModel : sqlmodel.SQLModel
        Base model for SQLModel.
    """

    id: int = Field(primary_key=True, index=True)
    username: str = Field(max_length=50, unique=True)
    password_hash: str = Field(max_length=100)
    role: UserRole
