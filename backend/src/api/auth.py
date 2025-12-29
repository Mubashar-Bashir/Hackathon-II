from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer
from typing import Dict, Any

from ..models.user import UserCreate, UserRead
from ..services.auth_service import AuthService
from ..storage.user_repository import UserRepository
from ..core.database import get_session_dep, Session
from ..core.security import security, authenticate_user_from_token, TokenData


router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_user_repository(session: Session = Depends(get_session_dep)):
    """Dependency to get user repository with session"""
    return UserRepository(session)


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)):
    """Dependency to get auth service with user repository"""
    return AuthService(user_repo)


@router.post("/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user account.
    """
    # Attempt to register the user
    created_user = auth_service.register_user(user_data)

    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    return {
        "user_id": str(created_user.id),
        "email": created_user.email,
        "message": "User registered successfully"
    }


@router.post("/login", response_model=Dict[str, Any])
async def login(
    username: str = Form(...),  # Using 'username' to match OAuth2 standard (can be email)
    password: str = Form(...),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate user and return JWT token.
    """
    # In our system, username is the email
    token_data = auth_service.login_user(username, password)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return token_data


@router.get("/me", response_model=UserRead)
async def get_current_user(
    token_data: TokenData = Depends(authenticate_user_from_token),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Get authenticated user information.
    """
    user = auth_service.get_current_user(token_data.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post("/logout", response_model=Dict[str, str])
async def logout():
    """
    Logout user and invalidate token (optional implementation).
    """
    # In a real implementation, you might want to add the token to a blacklist
    # For now, we just return a success message
    return {"message": "Successfully logged out"}