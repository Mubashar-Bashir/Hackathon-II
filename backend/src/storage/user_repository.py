from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from passlib.context import CryptContext

from .base_repository import BaseRepository
from ..models.user import User, UserRead, UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserRead, UserCreate, UserUpdate]):
    """
    Repository for User operations.
    Handles user creation, retrieval, and password hashing.
    """

    def __init__(self, session: Session):
        super().__init__(session)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        # Hash the password
        hashed_password = self.pwd_context.hash(user.password)

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
        return self.pwd_context.verify(plain_password, hashed_password)

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