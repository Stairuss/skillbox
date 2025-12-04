from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Кулинарная книга API", description="API для работы с рецептами")


@app.get("/recipes", response_model=List[schemas.RecipeList])
def read_recipes(db: Session = Depends(get_db)) -> List[schemas.RecipeList]:
    recipes = crud.get_all_recipes(db)
    return [
        schemas.RecipeList.model_validate(recipe)  # ← Автоматическая конвертация!
        for recipe in recipes
    ]


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeDetail)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)) -> schemas.RecipeDetail:
    recipe = crud.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    crud.increment_recipe_views(db, recipe)
    return schemas.RecipeDetail.model_validate(recipe)  # ← Автоматическая конвертация!


@app.post("/recipes", response_model=schemas.RecipeDetail)
def create_new_recipe(
    recipe: schemas.RecipeCreate, db: Session = Depends(get_db)
) -> schemas.RecipeDetail:
    db_recipe = crud.create_recipe(db, recipe)
    return schemas.RecipeDetail.model_validate(
        db_recipe
    )  # ← Автоматическая конвертация!
