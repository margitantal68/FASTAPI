import pytest
from fastapi.testclient import TestClient
from main import app, get_user_from_db

client = TestClient(app)

# --- Mock dependency ---
def mock_get_user(user_id: int):
    if user_id == 1:
        return {"id": 1, "name": "Mocked Alice"}
    return None

# --- Override dependency ---
app.dependency_overrides[get_user_from_db] = mock_get_user

# --- Tests ---
def test_read_user_success():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Mocked Alice"}

def test_read_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
