from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register", json={"nickname": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
