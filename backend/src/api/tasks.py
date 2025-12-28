from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any
from uuid import UUID

from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..services.task_service import TaskService
from ..storage.task_repository import TaskRepository
from ..core.database import get_session_dep, Session
from ..core.security import authenticate_user_from_token, TokenData


router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_repository(session: Session = Depends(get_session_dep)):
    """Dependency to get task repository with session"""
    return TaskRepository(session)


def get_task_service(task_repo: TaskRepository = Depends(get_task_repository)):
    """Dependency to get task service with task repository"""
    return TaskService(task_repo)


@router.get("/", response_model=Dict[str, Any])
async def get_tasks(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: str = Query(None, pattern="^(pending|in_progress|completed)$"),
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Get all tasks for the authenticated user with optional filtering.
    """
    tasks = task_service.get_tasks_for_user(
        user_id=UUID(token_data.user_id),
        offset=offset,
        limit=limit,
        status=status_filter
    )

    # In a real implementation, you'd want to get the total count separately
    # For now, just return the length of the current result
    total = len(tasks) if len(tasks) < limit else offset + len(tasks)  # Simplified
    return {
        "tasks": tasks,
        "total": total,
        "offset": offset,
        "limit": limit
    }


@router.get("/api/{user_id}/tasks", response_model=Dict[str, Any])
async def get_tasks_by_user_id(
    user_id: str,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: str = Query(None, pattern="^(pending|in_progress|completed)$"),
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Get all tasks for a specific user ID with optional filtering.
    Enforces that the user_id from JWT matches the {user_id} in the URL.
    """
    # Enforcement: Check if user_id from JWT matches the {user_id} in the URL
    if token_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own tasks"
        )

    # Validate UUID format
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    tasks = task_service.get_tasks_for_user(
        user_id=user_uuid,
        offset=offset,
        limit=limit,
        status=status_filter
    )

    # In a real implementation, you'd want to get the total count separately
    # For now, just return the length of the current result
    total = len(tasks) if len(tasks) < limit else offset + len(tasks)  # Simplified
    return {
        "tasks": tasks,
        "total": total,
        "offset": offset,
        "limit": limit
    }


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Create a new task for the authenticated user.
    """
    # Create a task for the authenticated user
    created_task = task_service.create_task_for_user(task, UUID(token_data.user_id))
    return created_task


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: UUID,
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    task = task_service.get_task_for_user(
        user_id=UUID(token_data.user_id),
        task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    return task


@router.get("/api/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def get_task_by_user_and_task_id(
    user_id: str,
    task_id: UUID,
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Get a specific task by user ID and task ID.
    Enforces that the user_id from JWT matches the {user_id} in the URL.
    """
    # Enforcement: Check if user_id from JWT matches the {user_id} in the URL
    if token_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own tasks"
        )

    # Validate UUID format
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    task = task_service.get_task_for_user(
        user_id=user_uuid,
        task_id=task_id
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Update a specific task for the authenticated user.
    """
    updated_task = task_service.update_task_for_user(
        user_id=UUID(token_data.user_id),
        task_id=task_id,
        task_update=task_update
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )

    return updated_task


@router.put("/api/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def update_task_by_user_and_task_id(
    user_id: str,
    task_id: UUID,
    task_update: TaskUpdate,
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Update a specific task by user ID and task ID.
    Enforces that the user_id from JWT matches the {user_id} in the URL.
    """
    # Enforcement: Check if user_id from JWT matches the {user_id} in the URL
    if token_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own tasks"
        )

    # Validate UUID format
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    updated_task = task_service.update_task_for_user(
        user_id=user_uuid,
        task_id=task_id,
        task_update=task_update
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )

    return updated_task


@router.delete("/{task_id}", response_model=Dict[str, str])
async def delete_task(
    task_id: UUID,
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Delete a specific task for the authenticated user.
    """
    success = task_service.delete_task_for_user(
        user_id=UUID(token_data.user_id),
        task_id=task_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )

    return {"message": "Task deleted successfully"}


@router.delete("/api/{user_id}/tasks/{task_id}", response_model=Dict[str, str])
async def delete_task_by_user_and_task_id(
    user_id: str,
    task_id: UUID,
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Delete a specific task by user ID and task ID.
    Enforces that the user_id from JWT matches the {user_id} in the URL.
    """
    # Enforcement: Check if user_id from JWT matches the {user_id} in the URL
    if token_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own tasks"
        )

    # Validate UUID format
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    success = task_service.delete_task_for_user(
        user_id=user_uuid,
        task_id=task_id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )

    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}", response_model=TaskRead)
async def toggle_task_completion(
    task_id: UUID,
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Toggle the completion status of a task for the authenticated user.
    """
    updated_task = task_service.toggle_task_completion(
        user_id=UUID(token_data.user_id),
        task_id=task_id
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )

    return updated_task


@router.patch("/api/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion_by_user_and_task_id(
    user_id: str,
    task_id: UUID,
    token_data: TokenData = Depends(authenticate_user_from_token),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Toggle the completion status of a task by user ID and task ID.
    Enforces that the user_id from JWT matches the {user_id} in the URL.
    """
    # Enforcement: Check if user_id from JWT matches the {user_id} in the URL
    if token_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own tasks"
        )

    # Validate UUID format
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    updated_task = task_service.toggle_task_completion(
        user_id=user_uuid,
        task_id=task_id
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )

    return updated_task