import pytest
from fastapi.testclient import TestClient
from backend.main import app
import sqlite3
import os

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    test_db = "/tmp/test.db"
    os.environ["DATABASE_URL"] = test_db
    yield
    if os.path.exists(test_db):
        os.remove(test_db)

def test_create_and_read_item(client):
    # Test creating an item
    response = client.post(
        "/items/",
        json={"name": "Test Item", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "Test Description"
    item_id = data["id"]

    # Test reading items
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == item_id
    assert data["items"][0]["name"] == "Test Item"