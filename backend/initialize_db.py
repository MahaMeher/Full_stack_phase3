#!/usr/bin/env python3
"""
Database initialization script for the Todo Backend API.
This script creates all required tables in the database.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from sqlmodel import SQLModel
from src.config.database import engine
from src.models.task import Task
from src.models.user import User
from src.models.conversation import Conversation
from src.models.message import Message

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")

    # Import all models to ensure they're registered with SQLModel
    # Task is already imported above

    # Create all tables
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()