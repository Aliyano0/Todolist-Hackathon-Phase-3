"""
Comprehensive test suite for Todo CRUD operations
Tests all endpoints without authentication requirements
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from database.session import get_session, create_db_and_tables
from sqlmodel import Session, SQLModel, create_engine
from models.todo import TodoTask
from core.services.todo_service import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    toggle_task_completion
)
from schemas.todo import TodoTaskCreate, TodoTaskUpdate


@pytest.fixture(scope="function")
def client():
    """Create a test client with a clean database for each test"""
    # Create an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)

    # Override the session dependency
    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()


def test_health_endpoint(client):
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Todo API is running" in data["message"]


def test_get_empty_todos_list(client):
    """Test getting an empty list of todos"""
    response = client.get("/api/todos")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"] == []


def test_create_todo_success(client):
    """Test creating a todo with valid data"""
    todo_data = {
        "title": "Test todo",
        "description": "Test description",
        "completed": False
    }

    response = client.post("/api/todos", json=todo_data)
    assert response.status_code == 201

    data = response.json()
    assert "data" in data
    created_todo = data["data"]

    assert created_todo["id"] is not None
    assert created_todo["id"] == "1"  # String ID as expected
    assert created_todo["title"] == "Test todo"
    assert created_todo["description"] == "Test description"
    assert created_todo["completed"] is False
    assert "createdAt" in created_todo
    assert "updatedAt" in created_todo


def test_create_todo_validation_error_empty_title(client):
    """Test creating a todo with empty title (should fail validation)"""
    todo_data = {
        "title": "",  # Empty title should fail
        "description": "Test description",
        "completed": False
    }

    response = client.post("/api/todos", json=todo_data)
    assert response.status_code == 400


def test_create_todo_validation_error_long_title(client):
    """Test creating a todo with too long title (should fail validation)"""
    todo_data = {
        "title": "A" * 256,  # Too long title should fail
        "description": "Test description",
        "completed": False
    }

    response = client.post("/api/todos", json=todo_data)
    assert response.status_code == 400


def test_get_single_todo(client):
    """Test getting a single todo by ID"""
    # First create a todo
    todo_data = {
        "title": "Test todo",
        "description": "Test description",
        "completed": False
    }

    create_response = client.post("/api/todos", json=todo_data)
    assert create_response.status_code == 201
    created_data = create_response.json()
    todo_id = created_data["data"]["id"]

    # Now get the todo
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    retrieved_todo = data["data"]

    assert retrieved_todo["id"] == todo_id
    assert retrieved_todo["title"] == "Test todo"
    assert retrieved_todo["description"] == "Test description"


def test_get_nonexistent_todo(client):
    """Test getting a todo that doesn't exist"""
    response = client.get("/api/todos/999")
    assert response.status_code == 404


def test_update_todo_success(client):
    """Test updating a todo with valid data"""
    # First create a todo
    todo_data = {
        "title": "Original title",
        "description": "Original description",
        "completed": False
    }

    create_response = client.post("/api/todos", json=todo_data)
    assert create_response.status_code == 201
    created_data = create_response.json()
    todo_id = created_data["data"]["id"]

    # Now update the todo
    update_data = {
        "title": "Updated title",
        "description": "Updated description",
        "completed": True
    }

    response = client.put(f"/api/todos/{todo_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    updated_todo = data["data"]

    assert updated_todo["id"] == todo_id
    assert updated_todo["title"] == "Updated title"
    assert updated_todo["description"] == "Updated description"
    assert updated_todo["completed"] is True


def test_update_nonexistent_todo(client):
    """Test updating a todo that doesn't exist"""
    update_data = {
        "title": "Updated title",
        "description": "Updated description",
        "completed": True
    }

    response = client.put("/api/todos/999", json=update_data)
    assert response.status_code == 404


def test_delete_todo_success(client):
    """Test deleting a todo successfully"""
    # First create a todo
    todo_data = {
        "title": "Test todo to delete",
        "description": "Test description",
        "completed": False
    }

    create_response = client.post("/api/todos", json=todo_data)
    assert create_response.status_code == 201
    created_data = create_response.json()
    todo_id = created_data["data"]["id"]

    # Verify the todo exists
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 200

    # Now delete the todo
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200

    # Verify the todo is gone
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_todo(client):
    """Test deleting a todo that doesn't exist"""
    response = client.delete("/api/todos/999")
    assert response.status_code == 404


def test_toggle_completion_success(client):
    """Test toggling completion status of a todo"""
    # First create a todo
    todo_data = {
        "title": "Test todo",
        "description": "Test description",
        "completed": False
    }

    create_response = client.post("/api/todos", json=todo_data)
    assert create_response.status_code == 201
    created_data = create_response.json()
    todo_id = created_data["data"]["id"]

    # Verify the todo is initially not completed
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 200
    initial_todo = get_response.json()["data"]
    assert initial_todo["completed"] is False

    # Toggle completion status
    response = client.patch(f"/api/todos/{todo_id}/complete")
    assert response.status_code == 200

    # Verify the todo is now completed
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 200
    toggled_todo = get_response.json()["data"]
    assert toggled_todo["completed"] is True

    # Toggle again to make sure it works both ways
    response = client.patch(f"/api/todos/{todo_id}/complete")
    assert response.status_code == 200

    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 200
    toggled_back_todo = get_response.json()["data"]
    assert toggled_back_todo["completed"] is False


def test_toggle_nonexistent_todo(client):
    """Test toggling completion status of a todo that doesn't exist"""
    response = client.patch("/api/todos/999/complete")
    assert response.status_code == 404


def test_get_multiple_todos(client):
    """Test getting multiple todos"""
    # Create multiple todos
    todo_data_1 = {"title": "First todo", "description": "First description", "completed": False}
    todo_data_2 = {"title": "Second todo", "description": "Second description", "completed": True}

    client.post("/api/todos", json=todo_data_1)
    client.post("/api/todos", json=todo_data_2)

    # Get all todos
    response = client.get("/api/todos")
    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    todos = data["data"]

    assert len(todos) == 2
    titles = [todo["title"] for todo in todos]
    assert "First todo" in titles
    assert "Second todo" in titles