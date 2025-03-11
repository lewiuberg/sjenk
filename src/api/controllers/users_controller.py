"""Controllers for the users endpoints."""

from typing import Any

from database import SessionDep
from database.models.user import User
from schemas.users import UserCreate, UserRead, UserUpdate
from sqlalchemy import Result
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar
from utils.logging import logger


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
    logger.debug(f"Creating user in the database: {user.username}")
    db_user = User(
        username=user.username,
        password_hash=user.password_hash,
        role=user.role,
    )
    try:
        session.add(instance=db_user)
        session.commit()
        session.refresh(instance=db_user)
        logger.debug(f"User created in the database: {db_user.username}")
    except IntegrityError as err:
        session.rollback()
        logger.error(f"IntegrityError while creating user: {err}")
        raise
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
    logger.debug("Reading all users from the database.")
    statement: SelectOfScalar[User] = select(User)
    result: Result[Any] = session.exec(statement)
    users = result.fetchall()
    logger.debug("Fetched all users from the database.")
    return users


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
    logger.debug(f"Reading user with ID {user_id} from the database.")
    db_user: User | None = session.get(entity=User, ident=user_id)
    if db_user is None:
        logger.warning(f"User with ID {user_id} not found in the database.")
        return None
    logger.debug(f"Fetched user with ID {user_id} from the database.")
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
    logger.debug(f"Updating user with ID {user_id} in the database.")
    db_user: User | None = session.get(entity=User, ident=user_id)
    if db_user is None:
        logger.warning(f"User with ID {user_id} not found in the database.")
        return None
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(instance=db_user)
    logger.debug(f"Updated user with ID {user_id} in the database.")
    return db_user
