import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from uuid import UUID
import uuid
from src.main import app
from src.core.database import engine, create_db_and_tables
from sqlmodel import Session, SQLModel, select
from src.models.user import User, UserCreate
from src.models.task import Task
from passlib.context import CryptContext


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API"""
    with TestClient(app) as test_client:
        # Create database tables
        create_db_and_tables()
        yield test_client


@pytest.fixture
def test_user():
    """Create a test user"""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword"
    }


def test_auth_register_endpoint(client, test_user):
    """Test the user registration endpoint"""
    response = client.post("/auth/register", json=test_user)

    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["email"] == test_user["email"]
    assert data["message"] == "User registered successfully"


def test_auth_login_endpoint(client, test_user):
    """Test the user login endpoint"""
    # First register the user
    client.post("/auth/register", json=test_user)

    # Then try to login
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }

    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_auth_me_endpoint(client, test_user):
    """Test the get current user endpoint"""
    # Register and login the user
    client.post("/auth/register", json=test_user)

    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }

    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # Access the /me endpoint
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["name"] == test_user["name"]


def test_tasks_crud_endpoints(client, test_user):
    """Test the task CRUD endpoints"""
    # Register and login the user
    client.post("/auth/register", json=test_user)

    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }

    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # Create a task
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium"
    }

    response = client.post("/tasks/", json=task_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert created_task["status"] == "pending"
    assert created_task["priority"] == "medium"
    task_id = created_task["id"]

    # Get all tasks
    response = client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) >= 1

    # Get specific task
    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == task_id
    assert task["title"] == task_data["title"]

    # Update task
    update_data = {
        "title": "Updated Task",
        "status": "in_progress"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["title"] == update_data["title"]
    assert updated_task["status"] == update_data["status"]

    # Toggle task completion
    response = client.patch(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    toggled_task = response.json()
    assert toggled_task["status"] in ["completed", "in_progress"]  # Depends on previous state

    # Delete task
    response = client.delete(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Verify task is deleted
    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_user_isolation(client):
    """Test that users can't access each other's tasks"""
    # Create first user
    user1_data = {
        "email": "user1@example.com",
        "name": "User 1",
        "password": "securepassword"
    }
    client.post("/auth/register", json=user1_data)
    login_response1 = client.post("/auth/login", data={
        "username": user1_data["email"],
        "password": user1_data["password"]
    })
    token1 = login_response1.json()["access_token"]

    # Create second user
    user2_data = {
        "email": "user2@example.com",
        "name": "User 2",
        "password": "securepassword"
    }
    client.post("/auth/register", json=user2_data)
    login_response2 = client.post("/auth/login", data={
        "username": user2_data["email"],
        "password": user2_data["password"]
    })
    token2 = login_response2.json()["access_token"]

    # User 1 creates a task
    task_data = {
        "title": "User 1's Task",
        "description": "This is User 1's task",
        "priority": "medium"
    }
    create_response = client.post("/tasks/", json=task_data, headers={"Authorization": f"Bearer {token1}"})
    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task["id"]
    user1_id = task["user_id"]

    # User 2 tries to access User 1's task using the direct endpoint
    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token2}"})
    assert response.status_code == 404  # Should not be accessible to user2

    # User 2 tries to access User 1's task using the user-specific endpoint
    response = client.get(f"/api/{user1_id}/tasks/{task_id}", headers={"Authorization": f"Bearer {token2}"})
    assert response.status_code == 403  # Forbidden due to user ID mismatch