from sqlalchemy.orm import Session
from models import Recipe
from typing import List, Optional


def get_all_recipes(db: Session) -> List[Recipe]:
    """Получить все рецепты из базы, отсортированные по просмотрам и времени"""
    return (
        db.query(Recipe)
        .order_by(Recipe.views_count.desc(), Recipe.cooking_time_minutes.asc())
        .all()
    )


def get_recipe_by_id(db: Session, recipe_id: int) -> Optional[Recipe]:
    """Получить один рецепт по ID"""
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def create_recipe(db: Session, recipe_data) -> Recipe:
    """Создать и сохранить новый рецепт в базе"""
    db_recipe = Recipe(
        name=recipe_data.name,
        cooking_time_minutes=recipe_data.cooking_time_minutes,
        ingredients=",".join(recipe_data.ingredients),
        description=recipe_data.description,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def increment_recipe_views(db: Session, recipe) -> None:
    """Увеличить счетчик просмотров рецепта на 1"""
    recipe.views_count += 1
    db.commit()
