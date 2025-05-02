from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Формируем URL для подключения к базе данных
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Определяем базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии БД


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
