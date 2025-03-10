"""Controllers for the users endpoints."""

from typing import Any

from database import SessionDep
from database.models.user import User
from fastapi import HTTPException
from schemas.users import UserCreate, UserRead, UserUpdate
from sqlalchemy import Result
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar


async def create_user_controller(
    user: UserCreate, session: SessionDep
) -> UserRead:
    """
    Create a user.

    Parameters
    ----------
    user : UserCreate
        The user to create.
    session : SessionDep
        The database session.

    Returns
    -------
    UserRead
        The created user.
    """
    db_user = User(
        username=user.username,
        password_hash=user.password_hash,
        role=user.role,
    )
    session.add(instance=db_user)
    session.commit()
    session.refresh(instance=db_user)
    return db_user


async def read_users_controller(session: SessionDep) -> list[UserRead]:
    """
    Read all users.

    Parameters
    ----------
    session : SessionDep
        The database session.

    Returns
    -------
    list[UserRead]
        The users.
    """
    statement: SelectOfScalar[User] = select(User)
    result: Result[Any] = session.exec(statement)
    return result.fetchall()


async def read_user_controller(user_id: int, session: SessionDep) -> UserRead:
    """
    Read a user.

    Parameters
    ----------
    user_id : int
        The user ID.
    session : SessionDep
        The database session.

    Returns
    -------
    UserRead
        The user.

    Raises
    ------
    HTTPException
        If the user is not found.
    """
    db_user: User | None = session.get(entity=User, ident=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


async def update_user_controller(
    user_id: int, user: UserUpdate, session: SessionDep
) -> UserRead:
    """
    Update a user.

    Parameters
    ----------
    user_id : int
        The user ID.
    user : UserUpdate
        The user to update.
    session : SessionDep
        The database session.

    Returns
    -------
    UserRead
        The updated user.

    Raises
    ------
    HTTPException
        If the user is not found.
    """
    db_user: User | None = session.get(entity=User, ident=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(instance=db_user)
    return db_user
