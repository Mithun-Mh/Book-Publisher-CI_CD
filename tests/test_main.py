
from fastapi.testclient import TestClient
from app.main import app, books

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_book():
    books.clear()

    response = client.post(
        "/books",
        json={
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "price": 2500
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Clean Code"
