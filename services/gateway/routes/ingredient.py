from fastapi import FastAPI, HTTPException ,  File, UploadFile, APIRouter, Depends
import fastapi as _fastapi
import requests
import models as _models
import os
import service as _service

ing_route = APIRouter()

BASE_URL = os.environ.get("INGREDIENT_SERVICE_HOST_URL")


@ing_route.get("/ingredients")
async def get_all_ingredients(token: str = Depends(_service.get_authorization_header)):
    try:
        return await _service.processRequest(f"{BASE_URL}/ingredients", 'GET', token)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@ing_route.post("/ingredients", tags=['Ingredients Service'])
async def create_ingredient(data: _models.IngredientCreate, token: str = Depends(_service.get_authorization_header)):
    try:
        serialized_data = {"name": data.name, "unit": data.unit, "amount": data.amount}
        return await _service.processRequest(f"{BASE_URL}/ingredients", 'POST', token=token, data=serialized_data)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@ing_route.get("/ingredients/{ing_id}", tags=['Ingredients Service'])
async def get_one_ingredient(ing_id: int, token: str = Depends(_service.get_authorization_header)):
    try:
        return await _service.processRequest(f"{BASE_URL}/ingredients/{ing_id}", 'GET', token=token)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
