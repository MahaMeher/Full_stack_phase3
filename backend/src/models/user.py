from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
import uuid
from typing import Optional


class UserBase(SQLModel):
    """Base model for User with common fields"""
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """User model for database table"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password_hash: str = Field(nullable=False)  # Store hashed passwords
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = Field(default=None)


class UserCreate(UserBase):
    """Model for creating a new user"""
    password: str  # Plain text password for creation/validation
    password_confirm: str  # Confirmation for validation


class UserUpdate(SQLModel):
    """Model for updating user information"""
    name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    is_active: Optional[bool] = Field(default=None)


class UserLogin(SQLModel):
    """Model for user login"""
    email: str
    password: str


class UserPublic(UserBase):
    """Model for public user information"""
    id: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]