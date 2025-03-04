"""Handle the database connection and session management."""

from typing import Annotated

from fastapi import Depends
from properties import config
from sqlmodel import Session, SQLModel, create_engine

from database.models.booking import Booking
from database.models.place import Place
from database.models.user import User

connect_args = {"check_same_thread": False}
engine = create_engine(
    config.database.url, echo=True, connect_args=connect_args
)


def create_db_and_tables():
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Get a session from the database.

    Yields
    ------
    Session
        A session from the database.
    """
    with Session(engine) as session:
        yield session


def dispose():
    """Dispose of the engine."""
    engine.dispose()


# Define a type alias for the database session dependency
SessionDep = Annotated[Session, Depends(get_session)]
