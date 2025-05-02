from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    players = relationship("PlayerSession", back_populates="game_session")
    grid_cells = relationship("GridCell", back_populates="game_session")
