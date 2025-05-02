# Схемы для игровой логики
from pydantic import BaseModel
from typing import List, Optional


class GameSessionCreate(BaseModel):
    """Схема для создания новой игровой сессии"""
    player_ids: List[int]  # Список ID игроков


class GameSessionResponse(BaseModel):
    """Схема для ответа о состоянии сессии"""
    id: int
    started: bool
    players: List[dict]  # [{nickname, color}, ...]
    grid: List[dict]  # [{x, y, color, player_id}, ...]


class WebSocketMessage(BaseModel):
    """Схема для сообщений через WebSocket"""
    type: str  # Тип сообщения: "join", "color_select", "click", "timer", "game_over"
    payload: dict  # Данные: {player_id, color, x, y, time_left, etc.}
