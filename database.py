from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models import Base

SQLALCHEMY_DATABASE_URL: str = "sqlite:///./recipes.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание всех таблиц описанных в Base (модели)
Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Возвращает сессию БД как генератор (FastAPI dependency)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
