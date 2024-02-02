# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_read_item():
    response = client.get("/item/foo")
    assert response.status_code == 200
    assert response.json() == {"item_id": "foo"}


def test_create_item():
    data = {"name": "Test Item"}
    response = client.post("/item/", json=data)
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item"}


def test_read_nonexistent_item():
    response = client.get("/item/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


# Add more tests as needed