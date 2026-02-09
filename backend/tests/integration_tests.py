"""
Basic integration tests for the Todo API
These tests verify that the API endpoints work correctly with the data transformations
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from models.todo import TodoTask
from database.session import get_session
from sqlmodel import Session, select


@pytest.fixture
def client():
    """Create a test client for the API"""
    with TestClient(app) as test_client:
        yield test_client


def test_get_todos_endpoint(client):
    """Test the GET /api/todos endpoint returns properly formatted data"""
    response = client.get("/api/todos")
    assert response.status_code == 200

    # Check that response is wrapped in 'data' property
    json_response = response.json()
    assert "data" in json_response
    assert isinstance(json_response["data"], list)


def test_create_todo_endpoint(client):
    """Test the POST /api/todos endpoint creates a todo with proper formatting"""
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False
    }

    response = client.post("/api/todos", json=todo_data)
    assert response.status_code == 201

    # Check that response is wrapped in 'data' property
    json_response = response.json()
    assert "data" in json_response

    # Check that the response has the expected fields in camelCase
    todo = json_response["data"]
    assert "id" in todo
    assert "title" in todo
    assert "description" in todo
    assert "completed" in todo
    assert "createdAt" in todo
    assert "updatedAt" in todo

    # Check that ID is a string
    assert isinstance(todo["id"], str)


def test_get_single_todo_endpoint(client):
    """Test the GET /api/todos/{id} endpoint returns properly formatted data"""
    # First create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False
    }

    create_response = client.post("/api/todos", json=todo_data)
    assert create_response.status_code == 201

    created_todo = create_response.json()["data"]
    todo_id = created_todo["id"]

    # Now get the specific todo
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200

    # Check that response is wrapped in 'data' property
    json_response = response.json()
    assert "data" in json_response

    # Check that the response has the expected fields in camelCase
    todo = json_response["data"]
    assert todo["id"] == todo_id
    assert isinstance(todo["id"], str)


def test_update_todo_endpoint(client):
    """Test the PUT /api/todos/{id} endpoint updates with proper formatting"""
    # First create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False
    }

    create_response = client.post("/api/todos", json=todo_data)
    assert create_response.status_code == 201

    created_todo = create_response.json()["data"]
    todo_id = created_todo["id"]

    # Now update the todo
    update_data = {
        "title": "Updated Todo",
        "completed": True
    }

    response = client.put(f"/api/todos/{todo_id}", json=update_data)
    assert response.status_code == 200

    # Check that response is wrapped in 'data' property
    json_response = response.json()
    assert "data" in json_response

    # Check that the response has the updated data
    updated_todo = json_response["data"]
    assert updated_todo["id"] == todo_id
    assert updated_todo["title"] == "Updated Todo"
    assert updated_todo["completed"] is True


def test_delete_todo_endpoint(client):
    """Test the DELETE /api/todos/{id} endpoint returns properly formatted data"""
    # First create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False
    }

    create_response = client.post("/api/todos", json=todo_data)
    assert create_response.status_code == 201

    created_todo = create_response.json()["data"]
    todo_id = created_todo["id"]

    # Now delete the todo
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200

    # Check that response is wrapped in 'data' property
    json_response = response.json()
    assert "data" in json_response

    # Check that the response has the deleted todo data
    deleted_todo = json_response["data"]
    assert deleted_todo["id"] == todo_id


def test_toggle_todo_completion_endpoint(client):
    """Test the PATCH /api/todos/{id}/toggle endpoint returns properly formatted data"""
    # First create a todo
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False
    }

    create_response = client.post("/api/todos", json=todo_data)
    assert create_response.status_code == 201

    created_todo = create_response.json()["data"]
    todo_id = created_todo["id"]

    # Now toggle the todo completion status
    response = client.patch(f"/api/todos/{todo_id}/toggle")
    assert response.status_code == 200

    # Check that response is wrapped in 'data' property
    json_response = response.json()
    assert "data" in json_response

    # Check that the response has the toggled todo data
    toggled_todo = json_response["data"]
    assert toggled_todo["id"] == todo_id