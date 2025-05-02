from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sys
import os

# Выводим текущую рабочую директорию и sys.path для диагностики
print("Текущая рабочая директория:", os.getcwd())
print("sys.path:", sys.path)

# Добавляем путь к /app/backend в sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_path)
print("Добавлен путь:", backend_path)

# Проверяем, существует ли папка app
app_path = os.path.join(backend_path, 'app')
print("Проверяем путь к app:", app_path,
      "существует:", os.path.exists(app_path))


# Импортируем Base из database.py
try:
    from app.database import Base
    print("Успешно импортирован app.database.Base")
except ImportError as e:
    print("Ошибка импорта app.database:", e)
    raise

# Импортируем модели, чтобы их метаданные загрузились
try:
    from app.models import User, GameSession, PlayerSession, GridCell
    print("Успешно импортированы модели")
except ImportError as e:
    print("Ошибка импорта моделей:", e)
    raise

# Загружаем конфигурацию из alembic.ini
config = context.config

# Настраиваем логирование
fileConfig(config.config_file_name)

# Подключаем переменные окружения
section = config.config_ini_section
config.set_section_option(
    section,
    "sqlalchemy.url",
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# Создаем подключение к базе данных
connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool
)

# Выполняем миграции
with connectable.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=Base.metadata
    )

    with context.begin_transaction():
        context.run_migrations()
