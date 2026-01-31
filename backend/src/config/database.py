from sqlmodel import create_engine, Session
from sqlalchemy import event
from contextlib import contextmanager
import os
from .settings import settings


# Create the database engine
# Use SQLite for local development if Neon DB is not configured properly
db_url = settings.neon_db_url

# Check if using a placeholder URL and switch to SQLite for development
# Only use SQLite if the URL contains placeholder values
if "ep-xxx" in db_url or "your_username" in db_url or "your_password" in db_url or "your_database_name" in db_url or db_url == "":
    # Use SQLite for local development
    db_url = "sqlite:///./todo_app_dev.db"
    print("Using SQLite for local development")

engine = create_engine(
    db_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before use
    # Add SQLite-specific settings if using SQLite
    connect_args={"check_same_thread": False} if "sqlite://" in db_url else {},
)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


# Optional: Add connection pooling settings
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite-specific pragmas if using SQLite"""
    if 'sqlite' in settings.neon_db_url:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()