from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
import hashlib
import secrets
from passlib.context import CryptContext
import logging

from .base_repository import BaseRepository
from ..models.user import User, UserRead, UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserRead, UserCreate, UserUpdate]):
    """
    Repository for User operations.
    Handles user creation, retrieval, and password hashing.
    """

    def __init__(self, session: Session):
        super().__init__(session)
        # Initialize bcrypt context with configuration that avoids the problematic internal tests
        # Use a more conservative approach to avoid the initialization issue
        try:
            self.pwd_context = CryptContext(
                schemes=["bcrypt"],
                deprecated="auto",
                bcrypt__ident="2b",
                bcrypt__rounds=12
            )
            # Test the context with a short password to ensure it works
            self.pwd_context.hash("test")
        except Exception as e:
            # If bcrypt initialization fails, log the error and continue with fallback
            logging.warning(f"bcrypt initialization failed: {e}. Using fallback PBKDF2.")
            self.pwd_context = None

    def _hash_password_with_bcrypt(self, password: str) -> str:
        """Hash password using bcrypt with length validation"""
        # Ensure password length is within bcrypt limits (72 bytes)
        if len(password) > 72:
            # Truncate password to 72 characters to avoid bcrypt error
            password = password[:72]
        return self.pwd_context.hash(password)

    def _verify_password_with_bcrypt(self, password: str, stored_hash: str) -> bool:
        """Verify password using bcrypt with length validation"""
        # Ensure password length is within bcrypt limits (72 bytes)
        if len(password) > 72:
            # Truncate password to 72 characters to avoid bcrypt error
            password = password[:72]
        return self.pwd_context.verify(password, stored_hash)

    def _hash_password_fallback(self, password: str) -> str:
        """Fallback password hashing using PBKDF2"""
        # Generate a random salt
        salt = secrets.token_hex(32)
        # Hash the password with the salt
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt.encode('utf-8'),
                                      100000)  # 100,000 iterations
        # Return salt + hash as a hex string
        return "pbkdf2$" + salt + pwdhash.hex()  # Prefix to identify the scheme

    def _verify_password_fallback(self, password: str, stored_hash: str) -> bool:
        """Fallback password verification for PBKDF2 hashes"""
        if not stored_hash.startswith("pbkdf2$"):
            return False
        # Remove the prefix
        stored_hash = stored_hash[7:]  # Remove "pbkdf2$" prefix
        # Extract salt (first 64 chars, since hex representation of 32-byte salt is 64 chars)
        salt = stored_hash[:64]
        stored_pwdhash = stored_hash[64:]

        # Hash the provided password with the same salt
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt.encode('utf-8'),
                                      100000)

        # Compare the hashes
        return secrets.compare_digest(stored_pwdhash, pwdhash.hex())

    @property
    def model(self) -> type[User]:
        return User

    @property
    def read_model(self) -> type[UserRead]:
        return UserRead

    def get_user_by_email(self, email: str) -> Optional[UserRead]:
        """Get a user by their email address"""
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).first()
        if result:
            return UserRead.model_validate(result)
        return None

    def create_user(self, user: UserCreate) -> UserRead:
        """Create a new user with hashed password"""
        # Use bcrypt if available, otherwise fallback to PBKDF2
        if self.pwd_context is not None:
            # Use bcrypt for password hashing
            hashed_password = self._hash_password_with_bcrypt(user.password)
        else:
            # Fallback to PBKDF2
            hashed_password = self._hash_password_fallback(user.password)

        # Create the user object with hashed password
        db_user = User(
            email=user.email,
            name=user.name,
            password_hash=hashed_password
        )

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return UserRead.model_validate(db_user)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against the hashed password"""
        # Check if this is a bcrypt hash (doesn't start with pbkdf2$)
        if hashed_password.startswith("pbkdf2$"):
            # Use fallback PBKDF2 verification
            return self._verify_password_fallback(plain_password, hashed_password)
        else:
            # Use bcrypt verification if context is available
            if self.pwd_context is not None:
                return self._verify_password_with_bcrypt(plain_password, hashed_password)
            else:
                # If bcrypt is not available and it's not a pbkdf2 hash, something is wrong
                return self._verify_password_fallback(plain_password, hashed_password)

    def authenticate_user(self, email: str, password: str) -> Optional[UserRead]:
        """Authenticate a user by email and password"""
        user = self.get_user_by_email(email)
        if not user:
            return None

        # Get the full user object to access password_hash
        db_user = self.session.exec(select(User).where(User.email == email)).first()
        if not db_user or not self.verify_password(password, db_user.password_hash):
            return None

        return UserRead.model_validate(db_user)