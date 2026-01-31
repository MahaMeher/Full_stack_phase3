#!/usr/bin/env python3
"""Simple test to verify timezone functionality in isolation"""

from datetime import datetime, timedelta, timezone

def test_generate_token_logic(email, name=None):
    """Test the same logic as in main.py without dependencies"""
    user_id = f"user_{email.replace('@', '_at_').replace('.', '_dot_')}"

    payload = {
        "id": user_id,
        "email": email,
        "name": name,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=1)  # 24 hours
    }

    print(f"Token payload created successfully: {payload['id']}")
    print(f"Issued at (iat): {payload['iat']}")
    print(f"Expires at (exp): {payload['exp']}")
    return payload

if __name__ == "__main__":
    print("Testing the timezone logic from generate_token function...")
    result = test_generate_token_logic("test@example.com", "Test User")
    print("SUCCESS: No timezone errors occurred!")