# services/ingredient_service/crud.py
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy.orm as _orm
import schemas as _schemas
import models as _models
from fastapi import HTTPException
import logging
from typing import List
import requests

logger = logging.getLogger(__name__)



async def create_ingredient_in_db(
    db: _orm.Session,
    ingredient: _schemas.IngredientCreate
) -> _models.Ingredient:
   
    try:
        # Create ingredient instance
        db_ingredient = _models.Ingredient(
            name=ingredient.name,
            unit=ingredient.unit,
            amount=ingredient.amount
        )
        
        # Add ingredient to database
        db.add(db_ingredient)
        # Commit the transaction
        db.commit()
        db.refresh(db_ingredient)
        
        
        logger.info(f"Successfully created ingredient with ID: {db_ingredient.id}")
        return db_ingredient
    
    except SQLAlchemyError as e:
        print(e)
        logger.error(f"Database error while creating ingredient: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the ingredient"
        )
    except Exception as e:
        print(e)
        logger.error(f"Unexpected error while creating ingredient: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
        
async def get_ingredient(ingredient_id: int, db: _orm.Session):
    try:
        # Create ingredient instance
        ingredient = db.query(_models.Ingredient).filter(_models.Ingredient.id == ingredient_id).first()
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        
        return ingredient
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while reading ingredient: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while reading the ingredient"
        )
    except Exception as e:
        logger.error(f"Unexpected error while reading ingredient: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
        
async def guery_ingredient(skip: int, limit: int, db: _orm.Session):
    try:
        # Create ingredient instance
        ingredient = db.query(_models.Ingredient).offset(skip).limit(limit).all()
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        
        return ingredient
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while reading ingredient: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while reading the ingredient"
        )
    except Exception as e:
        logger.error(f"Unexpected error while creareadingting ingredient: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )