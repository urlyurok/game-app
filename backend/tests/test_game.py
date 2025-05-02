from fastapi.testclient import TestClient
from ..app.main import app
import pytest

client = TestClient(app)


@pytest.mark.asyncio
async def test_websocket_connection():
    """Тест подключения к WebSocket"""
    with client.websocket_connect("/game/session/1") as websocket:
        # Проверяем, что соединение установлено
        assert websocket.accepted
        websocket.close()
