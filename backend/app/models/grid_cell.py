from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class GridCell(Base):
    __tablename__ = "grid_cells"

    id = Column(Integer, primary_key=True, index=True)
    game_session_id = Column(Integer, ForeignKey(
        "game_sessions.id"), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    color = Column(String(7), nullable=True)
    player_session_id = Column(Integer, ForeignKey(
        "player_sessions.id"), nullable=True)

    game_session = relationship("GameSession", back_populates="grid_cells")
    player_session = relationship("PlayerSession", back_populates="grid_cells")
