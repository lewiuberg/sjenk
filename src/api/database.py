"""Handle the database connection and session management."""

from models.booking import Booking  # noqa: F401
from models.place import Place  # noqa: F401
from models.user import User  # noqa: F401
from sqlmodel import Session, SQLModel, create_engine
from utils import config

DATABASE_URL = str(config.db.url)

connect_args = {"check_same_thread": False}
engine = create_engine(
    DATABASE_URL, echo=True, connect_args=connect_args
)


def create_db_and_tables():
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Return a new session.

    Returns
    -------
    Session : sqlmodel.Session
        A new session.
    """
    return Session(engine)
