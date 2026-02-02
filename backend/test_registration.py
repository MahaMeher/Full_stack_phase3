#!/usr/bin/env python3
"""
Test script to check user registration functionality
"""

import sys
import os
import asyncio
from sqlmodel import Session
from src.models.user import UserCreate
from src.services.user_service import UserService
from src.config.database import get_session

def test_registration():
    """Test user registration functionality"""
    print("Testing user registration...")

    # Create a database session
    session_generator = get_session()
    session = next(session_generator)  # Get the session from the generator

    try:
        # Create user service instance
        user_service = UserService()

        # Create test user data
        test_user_data = UserCreate(
            email=f"test_{os.getpid()}@example.com",  # Use PID to make email unique
            name="Test User",
            password="SecurePassword123!",
            password_confirm="SecurePassword123!"
        )

        print(f"Attempting to create user with email: {test_user_data.email}")

        # Try to create the user
        created_user = user_service.create_user(session, test_user_data)

        print(f"User created successfully!")
        print(f"User ID: {created_user.id}")
        print(f"Email: {created_user.email}")
        print(f"Name: {created_user.name}")
        print(f"Created at: {created_user.created_at}")

        # Verify the user exists in the database
        retrieved_user = user_service.get_user_by_email(session, test_user_data.email)
        if retrieved_user:
            print(f"Verification: User found in database with ID: {retrieved_user.id}")
        else:
            print("ERROR: User was not saved to database!")

    except Exception as e:
        print(f"Error during user registration: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    test_registration()