"""Handle the database connection and session management."""

from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends
from properties import config
from sqlmodel import Session, SQLModel, create_engine
from utils.logging import logger

from database.models.booking import Booking
from database.models.place import Place
from database.models.user import User

connect_args = {"check_same_thread": False}
engine = create_engine(
    config.database.url, echo=config.database.echo, connect_args=connect_args
)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    with engine.connect() as connection:
        existing_tables = connection.dialect.has_table(
            connection, "user"
        )  # Check for one of the tables
        if existing_tables:
            logger.info("Database and tables already exist.")
        else:
            logger.info("Creating database and tables...")
            SQLModel.metadata.create_all(engine)
            logger.info("Database and tables created.")


def get_session() -> Generator[Session, Any]:
    """
    Get a database session.

    Yields
    ------
    Generator[Session, Any]
        A database session.
    """
    logger.info("Creating a new database session...")
    with Session(engine) as session:
        try:
            yield session
        finally:
            logger.info("Closing the database session...")


def dispose() -> None:
    """Dispose of the engine."""
    logger.info("Disposing of the engine...")
    engine.dispose()
    logger.info("Engine disposed.")


# Define a type alias for the database session dependency
SessionDep = Annotated[Session, Depends(get_session)]
