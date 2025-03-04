"""Handle the database connection and session management."""

from models.booking import Booking  # noqa: F401
from models.place import Place  # noqa: F401
from models.user import User  # noqa: F401
from sqlmodel import Session, SQLModel, create_engine
from utils import config

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
