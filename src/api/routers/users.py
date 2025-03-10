"""User API routes."""

from controllers.users_controller import (
    create_user_controller,
    read_user_controller,
    read_users_controller,
    update_user_controller,
)
from database import SessionDep
from fastapi import APIRouter
from schemas.users import UserCreate, UserRead, UserUpdate

router = APIRouter(
    tags=["users"],
)


@router.post("/users/", response_model=UserRead)
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
    return await create_user_controller(user, session)


@router.get("/users/", response_model=list[UserRead])
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
    return await read_users_controller(session)


@router.get("/users/{user_id}", response_model=UserRead)
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
    return await read_user_controller(user_id, session)


@router.put("/users/{user_id}", response_model=UserRead)
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
    return await update_user_controller(user_id, user, session)
