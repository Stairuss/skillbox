from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Кулинарная книга API",
    description="API для работы с рецептами"
)


@app.get("/recipes", response_model=List[schemas.RecipeList])
def read_recipes(db: Session = Depends(get_db)) -> List[schemas.RecipeList]:
    """Возвращает список всех рецептов, отсортированный по популярности и времени."""
    return crud.get_all_recipes(db)


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeDetail)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)) -> schemas.RecipeDetail:
    """
    Возвращает детальную информацию по рецепту по ID.
    Увеличивает счетчик просмотров.
    """
    recipe = crud.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    crud.increment_recipe_views(db, recipe)

    return schemas.RecipeDetail(
        name=recipe.name,
        cooking_time_minutes=recipe.cooking_time_minutes,
        ingredients=recipe.ingredients.split(","),
        description=recipe.description,
    )


@app.post("/recipes", response_model=schemas.RecipeDetail)
def create_new_recipe(
    recipe: schemas.RecipeCreate, db: Session = Depends(get_db)
) -> schemas.RecipeDetail:
    """Создает новый рецепт и возвращает его детали."""
    db_recipe = crud.create_recipe(db, recipe)

    return schemas.RecipeDetail(
        name=db_recipe.name,
        cooking_time_minutes=db_recipe.cooking_time_minutes,
        ingredients=recipe.ingredients,
        description=db_recipe.description,
    )
