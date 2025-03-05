"""User API routes."""

from database import SessionDep
from database.models.user import User
from fastapi import APIRouter, HTTPException
from schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, session: SessionDep):
    """
    Register a new user.

    Parameters
    ----------
    user : UserCreate

        User data.

    session : SessionDep

        Database session.

    Returns
    -------
    UserRead

        User data.
    """
    db_user = User(
        username=user.username,
        password_hash=user.password_hash,
        role=user.role,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# get all users
@router.get("/users/", response_model=list[UserRead])
async def read_users(session: SessionDep):
    """
    Get all users.

    Parameters
    ----------
    session : SessionDep

        Database session.

    Returns
    -------
    list[UserRead]

        List of user data.
    """
    return session.query(User).all()


@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: SessionDep):
    """
    Get a user by ID.

    Parameters
    ----------
    user_id : int

        User ID.

    session : SessionDep

        Database session.

    Returns
    -------
    UserRead

        User data.

    Raises
    ------
    HTTPException

        User not found.
    """
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    """
    Update a user.

    Parameters
    ----------
    user_id : int

        User ID.

    user : UserUpdate

        User data.

    session : SessionDep

        Database session.

    Returns
    -------
    UserRead

        User data.

    Raises
    ------
    HTTPException

        User not found.
    """
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)
    return db_user
    # not getting updated in the database
    # db_user = session.qet(User, user_id)
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    # for key, value in user.dict(exclude_unset=True).items():
    #     setattr(db_user, key, value)
    # session.commit()
    # session.refresh(db_user)
    # return db_user
