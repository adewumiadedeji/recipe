import os
from typing import List
from fastapi import HTTPException, APIRouter
import fastapi as _fastapi
from utils.email_service import send_email
import sqlalchemy.orm as _orm
import service as _services
import schemas as _schemas
import models as _models
import logging
import utils.database as _database
from starlette.responses import RedirectResponse
import json




RECIPE_BASE_URL=os.getenv("RECIPE_SERVICE_HOST_URL") or None

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
@router.post("/rates/", response_model=_schemas.Rate)
async def create_recipe(
    rate: _schemas.RateCreate,
    db: _orm.Session = _fastapi.Depends(_database.get_db)
    ):
    try:
        # Get user ID from request state (set by auth middleware)
        
        # Create recipe
        db_rate = await _services.create_rate_in_db(
            db=db,
            rate=rate
        )
        
        return db_rate
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the recipe"
        )
        
        
@router.get("/rates/{recipe_id}", response_model=_schemas.RateResponse)
async def get_recipe_rate(
    recipe_id: int,
    db: _orm.Session = _fastapi.Depends(_database.get_db)
):
    recipe=await _services.get_recipe(RECIPE_BASE_URL, recipe_id)
    print(recipe)
    ratings=await _services.get_rating_by_recipe(recipe_id, db=db)
    
    # Calculate the mean rating
    rates = [item.rate for item in ratings]
    mean_rate = sum(rates) / len(rates) if rates else 0
    recipe={**recipe, "mean_rating": mean_rate}

    # recipe={**recipe, **mean_rate}
    # merged_list = [{**rating, **recipe} for rating in rates]
    return {**recipe, "ratings": ratings}