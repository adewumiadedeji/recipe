# services/rating_service/crud.py
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy.orm as _orm
from fastapi import HTTPException
import logging
from typing import List
import requests
import schemas as _schemas
import models as _models

logger = logging.getLogger(__name__)


async def get_recipe(base_url: str, recipe_id: int) -> _schemas.Recipe:
    try:
        print(f"{base_url}/recipes/{recipe_id}")
        response = requests.get(f"{base_url}/recipes/{recipe_id}")
        if response.status_code == 200:
            db_user = response.json()
            return db_user
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")



async def create_rate_in_db(
    db: _orm.Session,
    rate: _schemas.RateCreate,
) -> _models.Rating:
    
    try:
        # Create rate instance
        db_rate = _models.Rating(
            recipe_id=rate.recipe_id,
            rate=rate.rate
        )
        
        # Add rating to database
        db.add(db_rate)
        
        # Commit the transaction
        db.commit()
        db.refresh(db_rate)
        
        
        logger.info(f"Successfully created rating with ID: {db_rate.id}")
        return db_rate
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while creating rating: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the rating"
        )
    except Exception as e:
        logger.error(f"Unexpected error while creating rating: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
        
async def get_rating_by_recipe(recipe_id: int, db: _orm.Session):
    try:
        # Create rating instance
        rate = db.query(_models.Rating).filter(_models.Rating.recipe_id == recipe_id).all()
        if not rate:
            raise HTTPException(status_code=404, detail="Rating not found")
        
        return rate
    
    except SQLAlchemyError as e:
        print(e)
        logger.error(f"Database error while reading rating: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while reading the rating"
        )
    except Exception as e:
        print(e)
        logger.error(f"Unexpected error while reading rating: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
        