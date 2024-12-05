# services/mean plan_service/crud.py
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy.orm as _orm
from fastapi import HTTPException, Header
import logging
from typing import List
import requests
import schemas as _schemas
import models as _models

logger = logging.getLogger(__name__)

async def get_authorization_header(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    token = authorization.split(" ")[1]
    return token

async def get_current_user(base_url: str, token: str) -> str:
    try:
        headers = {"Authorization": f"Bearer {token}"}
        print("Headers: ", headers)
        response = requests.get(f"{base_url}/users/me", headers=headers)
        if response.status_code == 200:
            db_user = response.json()
            return db_user["id"]
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")



async def create_meal_in_db(
    db: _orm.Session,
    meal: _schemas.MealCreate,
    user_id: int,
) -> _models.MealPlan:
    
    try:
        # Create meal instance
        db_meal = _models.MealPlan(
            date=meal.date,
            meal_type=meal.meal_type,
            recipe_id=meal.recipe_id,
            user_id=user_id
        )
        
        # Add mean plan to database
        db.add(db_meal)
        
        # Commit the transaction
        db.commit()
        db.refresh(db_meal)
        
        
        logger.info(f"Successfully created mean plan with ID: {db_meal.id}")
        return db_meal
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating mean plan: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the mean plan"
        )
    except Exception as e:
        logger.error(f"Unexpected error while creating mean plan: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
        
async def get_meal_plan(plan_id: int, db: _orm.Session):
    try:
        # Create mean plan instance
        meal = db.query(_models.MealPlan).filter(_models.MealPlan.id == plan_id).first()
        if not meal:
            raise HTTPException(status_code=404, detail="Meal not found")
        
        return meal
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while reading mean plan: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while reading the mean plan"
        )
    except Exception as e:
        logger.error(f"Unexpected error while reading mean plan: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
        
async def guery_meal_plan(skip: int, limit: int, db: _orm.Session):
    try:
        # Create mean plan instance
        means = db.query(_models.MealPlan).offset(skip).limit(limit).all()
        if not means:
            raise HTTPException(status_code=404, detail="Meal not found")
        
        return means
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while reading mean plan: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while reading the mean plan"
        )
    except Exception as e:
        logger.error(f"Unexpected error while creareadingting mean plan: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )