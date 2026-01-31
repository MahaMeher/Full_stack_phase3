from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timezone
from ..models.user import User, UserCreate, UserUpdate, UserLogin
from ..utils.exceptions import UserNotFoundException, UserAlreadyExistsException, InvalidCredentialsException
from passlib.context import CryptContext
import re


class UserService:
    """
    Service class for user-related operations including authentication,
    user management, and password handling.
    """

    def __init__(self):
        # Configure password hashing context
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against

        Returns:
            bool: True if password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generate a hash for a plain text password.

        Args:
            password: Plain text password to hash

        Returns:
            str: Hashed password
        """
        return self.pwd_context.hash(password)

    def validate_email(self, email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email address to validate

        Returns:
            bool: True if email format is valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_password_strength(self, password: str) -> tuple[bool, str]:
        """
        Validate password strength.

        Args:
            password: Password to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit"

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"

        return True, ""

    def get_user_by_id(self, session: Session, user_id: str) -> Optional[User]:
        """
        Get a user by their ID.

        Args:
            session: Database session
            user_id: User ID to search for

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()

    def get_user_by_email(self, session: Session, email: str) -> Optional[User]:
        """
        Get a user by their email address.

        Args:
            session: Database session
            email: Email address to search for

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    def create_user(self, session: Session, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            session: Database session
            user_data: User creation data

        Returns:
            Created User object

        Raises:
            UserAlreadyExistsException: If email already exists
        """
        # Validate email format
        if not self.validate_email(user_data.email):
            raise ValueError("Invalid email format")

        # Check if user already exists
        existing_user = self.get_user_by_email(session, user_data.email)
        if existing_user:
            raise UserAlreadyExistsException(f"User with email {user_data.email} already exists")

        # Validate password strength
        is_valid, error_msg = self.validate_password_strength(user_data.password)
        if not is_valid:
            raise ValueError(error_msg)

        # Check password confirmation
        if user_data.password != user_data.password_confirm:
            raise ValueError("Passwords do not match")

        # Create password hash
        password_hash = self.get_password_hash(user_data.password)

        # Create user object
        user = User(
            email=user_data.email,
            name=user_data.name,
            password_hash=password_hash
        )

        # Add to session and commit
        session.add(user)
        try:
            session.commit()
            session.refresh(user)
        except Exception:
            session.rollback()
            raise

        return user

    def authenticate_user(self, session: Session, login_data: UserLogin) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            session: Database session
            login_data: User login credentials

        Returns:
            User object if authentication successful, None otherwise
        """
        # Get user by email
        user = self.get_user_by_email(session, login_data.email)

        # Check if user exists and password is correct
        if not user or not self.verify_password(login_data.password, user.password_hash):
            raise InvalidCredentialsException("Invalid email or password")

        if not user.is_active:
            raise InvalidCredentialsException("User account is deactivated")

        # Update last login time
        user.last_login = datetime.now(timezone.utc)
        session.add(user)
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

        return user

    def update_user(self, session: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """
        Update user information.

        Args:
            session: Database session
            user_id: ID of user to update
            user_update: Update data

        Returns:
            Updated User object if successful, None otherwise
        """
        user = self.get_user_by_id(session, user_id)

        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Update fields if provided
        update_data = user_update.dict(exclude_unset=True)

        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)

        user.updated_at = datetime.now(timezone.utc)

        session.add(user)
        try:
            session.commit()
            session.refresh(user)
        except Exception:
            session.rollback()
            raise

        return user

    def delete_user(self, session: Session, user_id: str) -> bool:
        """
        Delete a user.

        Args:
            session: Database session
            user_id: ID of user to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
        user = self.get_user_by_id(session, user_id)

        if not user:
            return False

        session.delete(user)
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

        return True