import os
from typing import List
from fastapi import HTTPException, APIRouter, Depends
import fastapi as _fastapi
from utils.email_service import send_email
import sqlalchemy.orm as _orm
import service as _services
import schemas as _schemas
import logging
import utils.database as _database
from starlette.responses import RedirectResponse
import json




AUTH_BASE_URL=os.getenv("AUTH_SERVICE_HOST_URL") or None

router = APIRouter()

@router.get("/")
def main():
    return RedirectResponse(url="/docs/")

@router.get("/health")
async def health_check():
    return {
        "service": "Recipe service",
        "status": "healthy",
        "version": "1.0.0",
        "dependencies": {
            "database": "up"
        }
    }
    

# Endpoint to check if the API is live
@router.post("/recipes", response_model=_schemas.Recipe)
async def create_recipe(
    recipe: _schemas.RecipeCreate,
    db: _orm.Session = _fastapi.Depends(_database.get_db),
    token: str = Depends(_services.get_authorization_header)
    ):
    try:
        # Get user ID from request state (set by auth middleware)
        user_id=await _services.get_current_user(AUTH_BASE_URL, token)
        print("User: ", user_id)
        # Create recipe
        db_recipe = await _services.create_recipe_in_db(
            db=db,
            recipe=recipe,
            user_id=user_id,
            # ingredient_ids=recipe.ingredients
        )
        
        return db_recipe
    
    except HTTPException:
        raise
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the recipe"
        )

@router.get("/recipes/{recipe_id}", response_model=_schemas.Recipe)
async def get_recipe(
    recipe_id: int,
    db: _orm.Session = _fastapi.Depends(_database.get_db)
):
    print("Recipe ID: ", recipe_id)
    return await _services.get_recipe(recipe_id, db=db)

@router.get("/recipes", response_model=List[_schemas.Recipe])
async def list_recipes(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_database.get_db)
):
    return await _services.guery_recipe(skip, limit, db=db)