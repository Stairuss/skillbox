from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
import pytest


client = TestClient(app)


def test_get_recipes():
    """Тест получения списка рецептов."""
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.fixture
def db_session():
    """Тестовая БД сессия."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
