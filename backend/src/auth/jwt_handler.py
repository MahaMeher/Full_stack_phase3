from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from fastapi import HTTPException, status
from ..config.settings import settings


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify JWT token, extracting user information.

    Args:
        token: JWT token string

    Returns:
        Dictionary containing user information if token is valid, None otherwise
    """
    try:
        # Decode the token using the secret from settings
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )

        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            return None

        return payload

    except jwt.PyJWTError:
        # Token is invalid
        return None


def extract_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID string if found and valid, None otherwise
    """
    payload = decode_token(token)
    if payload:
        # Better Auth typically stores user ID in 'id' or 'userId' field
        return payload.get("id") or payload.get("userId")
    return None


def verify_token(token: str) -> bool:
    """
    Verify if JWT token is valid.

    Args:
        token: JWT token string

    Returns:
        True if token is valid, False otherwise
    """
    return decode_token(token) is not None