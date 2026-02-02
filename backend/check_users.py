#!/usr/bin/env python3
"""
Script to check if users are being stored in the Neon database
"""

import asyncio
from sqlmodel import Session, select
from src.models.user import User
from src.config.database import get_session

def check_users_in_db():
    """Check if users exist in the database"""
    print("Checking users in database...")

    # Create a database session
    session_generator = get_session()
    session = next(session_generator)  # Get the session from the generator

    try:
        # Query all users
        statement = select(User)
        users = session.exec(statement).all()

        print(f"Found {len(users)} users in the database:")

        for user in users:
            print(f"- ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.name}")
            print(f"  Created: {user.created_at}")
            print(f"  Active: {user.is_active}")
            print()

        # Also check the raw table structure by attempting a simple query
        print("Database connection successful!")

    except Exception as e:
        print(f"Error querying database: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    check_users_in_db()