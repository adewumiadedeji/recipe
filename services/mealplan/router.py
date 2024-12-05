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
        "service": "Meal plan service",
        "status": "healthy",
        "version": "1.0.0",
        "dependencies": {
            "database": "up"
        }
    }
    

# Endpoint to check if the API is live
@router.post("/meal-plans", response_model=_schemas.Meal)
async def create_recipe(
    meal: _schemas.MealCreate,
    db: _orm.Session = _fastapi.Depends(_database.get_db),
    token: str = Depends(_services.get_authorization_header)
    ):
    try:
        # Get user ID from request state (set by auth middleware)
        user_id=await _services.get_current_user(AUTH_BASE_URL, token)
        
        
        
        # Create recipe
        db_recipe = await _services.create_meal_in_db(
            db=db,
            meal=meal,
            user_id=user_id
        )
        
        return db_recipe
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the recipe"
        )

@router.get("/meal-plans/{meal_id}", response_model=_schemas.Meal)
async def get_meal_plan(
    meal_id: int,
    db: _orm.Session = _fastapi.Depends(_database.get_db)
):
    
    return await _services.get_meal_plan(meal_id, db=db)

@router.get("/meal-plans", response_model=List[_schemas.Meal])
async def list_meal_plans(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_database.get_db)
):
    return await _services.guery_meal_plan(skip, limit, db=db)