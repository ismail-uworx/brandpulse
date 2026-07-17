"""
session.py — opens the door between your Python code and PostgreSQL.

This is the ONLY file that creates the actual database connection.
Every other file that needs to read/write data asks THIS file for a
session — nobody else connects directly. That way, if the connection
setup ever needs to change, there's exactly one place to fix it.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.utils.config import settings

# The engine is SQLAlchemy's core connection object — it knows HOW
# to talk to Postgres (via psycopg2, the driver you installed) but
# doesn't hold open a single connection; it manages a pool of them.
engine = create_engine(settings.database_url)

# SessionLocal is a FACTORY that creates new database sessions on
# demand. We don't create one global session — each request/operation
# gets its own, so concurrent operations don't interfere with each other.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class every table model (models.py) will inherit
# from. SQLAlchemy uses it to track which Python classes map to which
# SQL tables — this is how models.py and session.py stay connected.
Base = declarative_base()


def get_db():
    """
    Used later by FastAPI as a "dependency" — it hands each API request
    a fresh session, and the `finally` block guarantees it gets closed
    afterward, even if the request crashes partway through.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()