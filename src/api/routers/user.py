from database import SessionDep
from database.models.user import User
from fastapi import APIRouter, HTTPException
from schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


# @router.post("/users/", response_model=UserRead)
# async def create_user(user: UserCreate, session: SessionDep):
#     db_user = User.from_orm(user)
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
#     return db_user


@router.post("/users/", response_model=UserCreate)
async def create_user(user: UserCreate, session: SessionDep):
    db_user = User(
        username=user.username,
        password_hash=user.password_hash,
        role=user.role,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: SessionDep):
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)
    return db_user
