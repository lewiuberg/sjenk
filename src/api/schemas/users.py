"""User schemas."""

from database.models.user import UserRole
from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Base model for user.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
        Base model for Pydantic.
    """

    username: str
    password_hash: str
    role: UserRole


class UserCreate(UserBase):
    """
    Model for creating user.

    Parameters
    ----------
    UserBase : UserBase
        Base model for user.
    """

    pass


class UserUpdate(BaseModel):
    """
    Model for updating user.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
        Base model for Pydantic.
    """

    username: str | None = None
    password_hash: str | None = None
    role: UserRole | None = None


class UserRead(BaseModel):
    """
    Model for reading user.

    Parameters
    ----------
    BaseModel : pydantic.BaseModel
        Base model for Pydantic.
    """

    id: int
    username: str
    role: UserRole

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class UserDelete(UserBase):
    """
    Model for deleting user.

    Parameters
    ----------
    UserBase : UserBase
        Base model for user.
    """

    id: int
