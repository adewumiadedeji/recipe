# services/recipe_service/crud.py
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
        response = requests.get(f"{base_url}/users/me", headers=headers)
        if response.status_code == 200:
            db_user = response.json()
            return db_user["id"]
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError as e:
        print("Exception: ", e)
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")

async def create_recipe_in_db(
    db: _orm.Session,
    recipe: _schemas.RecipeCreate,
    user_id: int,
    ingredient_ids: List[int] = None
) -> _models.Recipe:
    
    try:
        # Create recipe instance
        db_recipe = _models.Recipe(
            title=recipe.title,
            description=recipe.description,
            instructions=recipe.instructions,
            user_id=user_id
        )
        
        # Add recipe to database
        db.add(db_recipe)
        db.flush()  # Flush to get the recipe ID
        
        # If ingredient IDs are provided, associate them with the recipe
        if ingredient_ids:
            # Verify all ingredients exist
            # ingredients = db.query(_models.Ingredient).filter(
            #     _models.Ingredient.id.in_(ingredient_ids)
            # ).all()
            
            # if len(ingredients) != len(ingredient_ids):
            #     raise HTTPException(
            #         status_code=400,
            #         detail="One or more ingredient IDs are invalid"
            #     )
            
            # Associate ingredients with recipe
            db_recipe.ingredients = ingredient_ids
        
        # Commit the transaction
        db.commit()
        db.refresh(db_recipe)
        
        
        logger.info(f"Successfully created recipe with ID: {db_recipe.id}")
        return db_recipe
    
    except SQLAlchemyError as e:
        print(e)
        logger.error(f"Database error while creating recipe: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the recipe"
        )
    except Exception as e:
        print(e)
        logger.error(f"Unexpected error while creating recipe: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
        
async def get_recipe(recipe_id: int, db: _orm.Session):
    try:
    
        # Create recipe instance
        recipe = db.query(_models.Recipe).filter(_models.Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        return recipe
    
    except SQLAlchemyError as e:
        print(e)
        logger.error(f"Database error while reading recipe: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while reading the recipe"
        )
    except Exception as e:
        print(e)
        logger.error(f"Unexpected error while reading recipe: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
        
async def guery_recipe(skip: int, limit: int, db: _orm.Session):
    try:
        # Create recipe instance
        recipe = db.query(_models.Recipe).offset(skip).limit(limit).all()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        return recipe
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while reading recipe: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An error occurred while reading the recipe"
        )
    except Exception as e:
        logger.error(f"Unexpected error while creareadingting recipe: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )