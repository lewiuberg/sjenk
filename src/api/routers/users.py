"""User API routes."""

from controllers.users_controller import (
    create_user_controller,
    read_user_controller,
    read_users_controller,
    update_user_controller,
)
from database import SessionDep
from fastapi import APIRouter, HTTPException, status
from schemas.users import UserCreate, UserRead, UserUpdate
from sqlalchemy.exc import IntegrityError
from utils.logging import logger

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def read_users(session: SessionDep) -> list[UserRead]:
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
    logger.info("Fetching all users.")
    users = await read_users_controller(session)
    logger.info("Fetched all users successfully.")
    return users


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: SessionDep) -> UserRead:
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
    logger.info(f"Creating user with username: {user.username}")
    try:
        created_user = await create_user_controller(user, session)
        logger.info(f"User created successfully: {created_user.username}")
        return created_user
    except IntegrityError as err:
        logger.error(f"Failed to create user: {err}")
        raise HTTPException(
            status_code=400, detail="Username already exists"
        ) from err


@router.get(
    "/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK
)
async def read_user(user_id: int, session: SessionDep) -> UserRead:
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
    """
    logger.info(f"Fetching user with ID: {user_id}")
    db_user = await read_user_controller(user_id, session)
    if db_user is None:
        logger.warning(f"User with ID {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user id {user_id} not found",
        )
    logger.info(f"Fetched user with ID: {user_id} successfully.")
    return db_user


@router.put(
    "/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK
)
async def update_user(
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

        The database session

    Returns
    -------
    UserRead

        The updated user.
    """
    logger.info(f"Updating user with ID: {user_id}")
    db_user = await update_user_controller(user_id, user, session)
    if db_user is None:
        logger.warning(f"User with ID {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user id {user_id} not found",
        )
    logger.info(f"Updated user with ID: {user_id} successfully.")
    return db_user
