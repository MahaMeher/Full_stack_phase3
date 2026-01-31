#!/usr/bin/env python3
"""Debug script to test timezone import and usage"""

print("Starting debug script...")

try:
    from datetime import datetime, timedelta, timezone
    print("+ Successfully imported timezone from datetime")
    print(f"  timezone.utc = {timezone.utc}")
except ImportError as e:
    print(f"- Failed to import timezone: {e}")

try:
    # Test the exact same operation as in main.py
    now = datetime.now(timezone.utc)
    print(f"+ Successfully used datetime.now(timezone.utc): {now}")
except NameError as e:
    print(f"- Failed to use timezone.utc: {e}")

print("\nTrying to import and test the generate_token function:")
try:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

    # Import the module
    from src.main import generate_token
    print("+ Successfully imported generate_token function")

    # Try to call it with sample data (this will fail for other reasons but test the timezone)
    try:
        # We'll catch the error to see if it's the timezone issue or something else
        result = generate_token(email="test@example.com", name="Test User")
        print(f"Function call succeeded: {result}")
    except Exception as e:
        # Check if the error contains 'timezone' in it
        error_str = str(e)
        if 'timezone' in error_str or 'name \'timezone\' is not defined' in error_str:
            print(f"- Still getting timezone error: {e}")
        else:
            print(f"Different error (expected): {type(e).__name__}: {e}")

except ImportError as e:
    print(f"- Failed to import generate_token: {e}")