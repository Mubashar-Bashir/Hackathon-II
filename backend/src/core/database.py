from sqlmodel import create_engine, Session, SQLModel
from contextlib import contextmanager
from typing import Generator
import os

from .config import settings


# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True to see SQL queries in logs
    pool_pre_ping=True,  # Verify connections before use
)


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    This should be called when starting the application.
    """
    SQLModel.metadata.create_all(engine)


def get_session_context() -> Generator[Session, None, None]:
    """
    Context manager to get a database session.
    Automatically handles session creation and cleanup.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session_dep() -> Generator[Session, None, None]:
    """
    Function to get a database session (for dependency injection).
    """
    session = Session(engine)
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()