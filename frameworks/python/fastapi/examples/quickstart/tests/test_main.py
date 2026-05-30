from fastapi.testclient import TestClient

from main import app, repository


client = TestClient(app)


def setup_function() -> None:
    repository.reset()


def test_list_books() -> None:
    response = client.get("/books")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "FastAPI type driven APIs"


def test_create_and_read_book() -> None:
    create_response = client.post(
        "/books",
        json={"title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"},
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 2

    read_response = client.get(f"/books/{created['id']}")
    assert read_response.status_code == 200
    assert read_response.json()["author"] == "Martin Kleppmann"


def test_missing_book_returns_404() -> None:
    response = client.get("/books/404")

    assert response.status_code == 404
    assert response.json()["detail"] == "book not found"


def test_openapi_contains_models() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    schemas = response.json()["components"]["schemas"]
    assert "BookCreate" in schemas
    assert "BookRead" in schemas
