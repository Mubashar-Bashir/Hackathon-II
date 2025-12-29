import logging
from typing import Optional
from datetime import timedelta
from uuid import UUID

from ..models.user import UserCreate, UserRead
from ..storage.user_repository import UserRepository
from ..core.security import create_access_token
from ..core.config import settings


class AuthService:
    """
    Authentication service for handling user registration, login, and JWT token generation.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def register_user(self, user_data: UserCreate) -> Optional[UserRead]:
        """
        Register a new user.
        Returns the created user if successful, None if user already exists.
        """
        self.logger.info(f"Attempting to register user with email: {user_data.email}")

        # Check if user already exists
        existing_user = self.user_repository.get_user_by_email(user_data.email)
        if existing_user:
            self.logger.warning(f"Registration failed: User with email {user_data.email} already exists")
            return None  # User already exists

        # Create the new user
        created_user = self.user_repository.create_user(user_data)
        if created_user:
            self.logger.info(f"Successfully registered user with ID: {created_user.id}")

        return created_user

    def login_user(self, email: str, password: str) -> Optional[dict]:
        """
        Authenticate user and return JWT token.
        Returns token data if authentication is successful, None otherwise.
        """
        self.logger.info(f"Login attempt for user: {email}")

        user = self.user_repository.authenticate_user(email, password)
        if not user:
            self.logger.warning(f"Login failed for user: {email}")
            return None

        # Create access token
        access_token_expires = timedelta(hours=settings.jwt_expiration_hours)
        access_token = create_access_token(
            data={"user_id": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        self.logger.info(f"Successfully authenticated user: {email} (ID: {user.id})")

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.jwt_expiration_hours * 3600  # Convert to seconds
        }

    def get_current_user(self, user_id: str) -> Optional[UserRead]:
        """
        Get user information by user ID.
        """
        self.logger.debug(f"Retrieving user information for ID: {user_id}")

        # Convert string ID to UUID for database query
        try:
            uuid_user_id = UUID(user_id)
        except ValueError:
            self.logger.error(f"Invalid user ID format: {user_id}")
            return None

        # Retrieve user from database
        user = self.user_repository.get_by_id(uuid_user_id)
        if user:
            self.logger.debug(f"Successfully retrieved user: {user.email} (ID: {user.id})")
        else:
            self.logger.warning(f"User not found for ID: {user_id}")

        return user