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
    return await read_users_controller(session)


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
    try:
        return await create_user_controller(user, session)
    except IntegrityError as err:
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
    db_user = await read_user_controller(user_id, session)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user id {user_id} not found",
        )
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
    # return await update_user_controller(user_id, user, session)
    db_user = await update_user_controller(user_id, user, session)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with user id {user_id} not found",
        )
    return db_user
