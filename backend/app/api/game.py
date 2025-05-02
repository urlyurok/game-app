from fastapi import APIRouter, WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db
from app.models import User, GameSession, PlayerSession, GridCell
from app.schemas.game import WebSocketMessage
from typing import List
import json
import asyncio

router = APIRouter(prefix="/game", tags=["game"])

# Хранилище активных WebSocket-соединений для каждой сессии
active_sessions = {}


@router.websocket("/session/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: int, db: Session = Depends(get_db)):
    """WebSocket для игровой сессии"""
    await websocket.accept()

    # Проверяем существование сессии
    session = db.query(GameSession).filter(
        GameSession.id == session_id).first()
    if not session:
        await websocket.close(code=1008, reason="Сессия не найдена")
        return

    # Инициализируем сессию в active_sessions, если её нет
    if session_id not in active_sessions:
        active_sessions[session_id] = {
            "connections": [],
            "colors": set(),  # Храним занятые цвета
            # Состояние сетки 10x10
            "grid": {(x, y): None for x in range(10) for y in range(10)},
            "players": {},  # {player_id: {nickname, color}}
            "timer_started": False
        }

    session_data = active_sessions[session_id]
    session_data["connections"].append(websocket)

    try:
        # Обрабатываем сообщения от клиента
        while True:
            data = await websocket.receive_text()
            message = WebSocketMessage(**json.loads(data))

            if message.type == "join":
                # Игрок присоединяется к сессии
                player_id = message.payload["player_id"]
                nickname = db.query(User).filter(
                    User.id == player_id).first().nickname
                session_data["players"][player_id] = {
                    "nickname": nickname, "color": None}

                # Отправляем текущее состояние сессии
                await broadcast(session_id, {
                    "type": "state",
                    "payload": {
                        "players": session_data["players"],
                        "grid": session_data["grid"],
                        "time_left": 15 if not session_data["timer_started"] else 0
                    }
                })

                # Запускаем таймер, если 4 игрока
                if len(session_data["players"]) == 4 and not session_data["timer_started"]:
                    session_data["timer_started"] = True
                    asyncio.create_task(start_timer(session_id, db))

            elif message.type == "color_select":
                # Игрок выбирает цвет
                color = message.payload["color"]
                player_id = message.payload["player_id"]

                # Проверяем, что цвет уникален
                if color not in session_data["colors"]:
                    session_data["colors"].add(color)
                    session_data["players"][player_id]["color"] = color
                    db_player = db.query(PlayerSession).filter(
                        PlayerSession.game_session_id == session_id,
                        PlayerSession.user_id == player_id
                    ).first()
                    db_player.color = color
                    db.commit()

                    await broadcast(session_id, {
                        "type": "color_selected",
                        "payload": {"player_id": player_id, "color": color}
                    })
                else:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "payload": {"message": "Этот цвет уже занят"}
                    }))

            elif message.type == "click":
                # Игрок кликает на ячейку
                x, y = message.payload["x"], message.payload["y"]
                player_id = message.payload["player_id"]

                # Проверяем, свободна ли ячейка
                if session_data["grid"][(x, y)] is None:
                    color = session_data["players"][player_id]["color"]
                    session_data["grid"][(x, y)] = {
                        "color": color, "player_id": player_id}

                    # Обновляем статистику в БД
                    db_player = db.query(PlayerSession).filter(
                        PlayerSession.game_session_id == session_id,
                        PlayerSession.user_id == player_id
                    ).first()
                    db_player.successful_clicks += 1
                    db_player.total_clicks += 1
                    db_cell = GridCell(
                        game_session_id=session_id,
                        x=x, y=y,
                        color=color,
                        player_session_id=db_player.id
                    )
                    db.add(db_cell)
                    db.commit()

                    await broadcast(session_id, {
                        "type": "cell_updated",
                        "payload": {"x": x, "y": y, "color": color, "player_id": player_id}
                    })
                else:
                    # Неуспешный клик
                    db_player = db.query(PlayerSession).filter(
                        PlayerSession.game_session_id == session_id,
                        PlayerSession.user_id == player_id
                    ).first()
                    db_player.unsuccessful_clicks += 1
                    db_player.total_clicks += 1
                    db.commit()

    except Exception as e:
        print(f"Ошибка WebSocket: {e}")
    finally:
        session_data["connections"].remove(websocket)
        if not session_data["connections"]:
            del active_sessions[session_id]


async def broadcast(session_id: int, message: dict):
    """Отправка сообщения всем клиентам в сессии"""
    if session_id in active_sessions:
        for connection in active_sessions[session_id]["connections"]:
            await connection.send_text(json.dumps(message))


async def start_timer(session_id: int, db: Session):
    """Запуск 15-секундного таймера перед началом игры"""
    for i in range(15, -1, -1):
        await broadcast(session_id, {
            "type": "timer",
            "payload": {"time_left": i}
        })
        await asyncio.sleep(1)

    # Игра началась
    session = db.query(GameSession).filter(
        GameSession.id == session_id).first()
    session.started_at = func.now()
    db.commit()

    # Здесь можно добавить логику завершения игры (например, через 60 секунд)
