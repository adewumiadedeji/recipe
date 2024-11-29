import os
from typing import List
from fastapi import HTTPException, APIRouter
import fastapi as _fastapi
from utils.email_service import send_email
import sqlalchemy.orm as _orm
import models as _models
import service as _services
import schemas as _schemas
import logging
import utils.database as _database
from starlette.responses import RedirectResponse
import json



router = APIRouter()

@router.get("/")
def main():
    return RedirectResponse(url="/docs/")

@router.get("/health")
async def health_check():
    return {
        "service": "Ingredient service",
        "status": "healthy",
        "version": "1.0.0",
        "dependencies": {
            "database": "up"
        }
    }
    

# Endpoint to check if the API is live
@router.post("/ingredients", response_model=_schemas.Ingredient)
async def create_ingredient(
    ingredient: _schemas.IngredientCreate,
    db: _orm.Session = _fastapi.Depends(_database.get_db)
    ):
    
   
    try:
        # Create recipe
        db_ingredient = await _services.create_ingredient_in_db(
            db=db,
            ingredient=ingredient
        )
        
        return db_ingredient
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the ingredient"
        )

@router.get("/ingredients/{ingredient_id}", response_model=_schemas.Ingredient)
async def get_ingridient(
    ingredient_id: int,
    db: _orm.Session = _fastapi.Depends(_database.get_db)
):
    return await _services.get_ingredient(ingredient_id, db=db)

@router.get("/ingredients", response_model=List[_schemas.Ingredient])
async def list_recipes(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_database.get_db)
):
   
    return await _services.guery_ingredient(skip, limit, db=db)