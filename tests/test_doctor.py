from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_doctor():
    response = client.post(
        "/doctors",
        json={
            "name": "Dr Test",
            "specialization": "General",
            "availability": "Monday"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Dr Test"