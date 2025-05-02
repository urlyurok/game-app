from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, PlayerSession
from app.utils.auth import get_current_user
from typing import Dict

router = APIRouter(prefix="/player", tags=["player"])


@router.get("/stats", response_model=Dict)
def get_player_stats(nickname: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Получение статистики игрока"""
    user = db.query(User).filter(User.nickname == nickname).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    sessions = db.query(PlayerSession).filter(
        PlayerSession.user_id == user.id).all()
    total_games = len(sessions)
    total_clicks = sum(s.total_clicks for s in sessions)
    successful_clicks = sum(s.successful_clicks for s in sessions)
    unsuccessful_clicks = sum(s.unsuccessful_clicks for s in sessions)

    # Находим наиболее частый цвет
    color_counts = db.query(PlayerSession.color, func.count(PlayerSession.color)).filter(
        PlayerSession.user_id == user.id
    ).group_by(PlayerSession.color).order_by(func.count(PlayerSession.color).desc()).first()
    favorite_color = color_counts[0] if color_counts else None

    return {
        "total_games": total_games,
        "total_clicks": total_clicks,
        "successful_clicks": successful_clicks,
        "unsuccessful_clicks": unsuccessful_clicks,
        "favorite_color": favorite_color
    }
