import pytest
from fastapi.testclient import TestClient
import sqlite3
import os
from importlib import reload
from backend import main

@pytest.fixture
def client(tmp_path):
    test_db = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = str(test_db)
    
    # モジュールをリロードして新しいアプリインスタンスを作成
    reload(main)
    from backend.main import app
    
    # テスト用テーブル作成
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()
    
    # 新しいアプリインスタンスを使用
    test_app = main.app
    
    yield TestClient(test_app)
    
    # テスト後にデータベースファイルを削除
    if test_db.exists():
        test_db.unlink()

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

def test_create_multiple_items(client):
    # Create first item
    response1 = client.post(
        "/items/",
        json={"name": "Item 1", "description": "Description 1"}
    )
    assert response1.status_code == 200
    
    # Create second item
    response2 = client.post(
        "/items/",
        json={"name": "Item 2", "description": "Description 2"}
    )
    assert response2.status_code == 200

    # Verify both items exist
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert {item["name"] for item in data["items"]} == {"Item 1", "Item 2"}

def test_get_nonexistent_item(client):
    response = client.get("/items/999")  # Non-existent ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_create_item_with_invalid_data(client):
    # Missing required 'name' field
    response = client.post(
        "/items/",
        json={"description": "Invalid item"}
    )
    assert response.status_code == 422
    assert "name" in response.json()["detail"][0]["loc"]

def test_database_transaction_rollback(client):
    # Test that failed transaction doesn't persist data
    try:
        # This will fail due to missing name
        client.post("/items/", json={"description": "Should rollback"})
    except:
        pass
    
    # Verify no items were created
    response = client.get("/items/")
    assert len(response.json()["items"]) == 0

def test_concurrent_database_access(client):
    import threading
    
    def create_item(name):
        response = client.post(
            "/items/",
            json={"name": name, "description": f"Description for {name}"}
        )
        assert response.status_code == 200
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=create_item, args=(f"Item-{i}",))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    response = client.get("/items/")
    assert len(response.json()["items"]) == 5

def test_large_data_volume(client):
    # Test inserting and retrieving large amount of data
    for i in range(100):
        response = client.post(
            "/items/",
            json={"name": f"Item {i}", "description": "X"*1000}
        )
        assert response.status_code == 200
    
    response = client.get("/items/")
    assert len(response.json()["items"]) == 100
    assert len(response.json()["items"][0]["description"]) == 1000

def test_special_characters(client):
    # Test handling of special characters
    special_text = "テスト 漢字 !@#$%^&*()"
    response = client.post(
        "/items/",
        json={"name": special_text, "description": special_text}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == special_text
    assert data["description"] == special_text