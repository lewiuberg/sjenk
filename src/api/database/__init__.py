"""Handle the database connection and session management."""

from collections.abc import Generator
from typing import Annotated, Any

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


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any]:
    """
    Get a database session.

    Yields
    ------
    Generator[Session, Any]
        A database session.
    """
    with Session(engine) as session:
        yield session


def dispose() -> None:
    """Dispose of the engine."""
    engine.dispose()


# Define a type alias for the database session dependency
SessionDep = Annotated[Session, Depends(get_session)]
