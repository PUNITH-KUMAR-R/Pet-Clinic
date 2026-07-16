from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_pet():
    response = client.post(
        "/pets",
        json={
            "name": "Bella",
            "species": "Dog",
            "owner": "Punith"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Bella"