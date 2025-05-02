from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class PlayerSession(Base):
    __tablename__ = "player_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_session_id = Column(Integer, ForeignKey(
        "game_sessions.id"), nullable=False)
    color = Column(String(7), nullable=False)  # HEX-код, например #FF0000
    total_clicks = Column(Integer, nullable=False, default=0)
    successful_clicks = Column(Integer, nullable=False, default=0)
    unsuccessful_clicks = Column(Integer, nullable=False, default=0)
    is_winner = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="game_sessions")
    game_session = relationship("GameSession", back_populates="players")
    grid_cells = relationship("GridCell", back_populates="player_session")
