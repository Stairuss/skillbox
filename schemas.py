from pydantic import BaseModel
from typing import List


class RecipeList(BaseModel):
    """Модель для списка рецептов (GET /recipes)."""

    name: str
    views_count: int
    cooking_time_minutes: int

    class Config:
        orm_mode = True


class RecipeDetail(BaseModel):
    """Модель с деталями рецепта (GET /recipes/{id})."""

    name: str
    cooking_time_minutes: int
    ingredients: List[str]
    description: str

    class Config:
        orm_mode = True


class RecipeCreate(BaseModel):
    """Модель для создания нового рецепта (POST /recipes)."""

    name: str
    cooking_time_minutes: int
    ingredients: List[str]
    description: str
