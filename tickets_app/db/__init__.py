"""Database initialization and session utilities."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import config
from .models import Base

engine = create_engine(config.DB_URL)
Session = sessionmaker(bind=engine)


def init_db():
    """Create database tables."""
    Base.metadata.create_all(engine)
