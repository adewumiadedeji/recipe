from fastapi import FastAPI, HTTPException ,  File, UploadFile, APIRouter, Depends
import fastapi as _fastapi
import requests
import models as _models
import os
import service as _service

recipe_route = APIRouter()

BASE_URL = os.environ.get("RECIPE_SERVICE_HOST_URL")


@recipe_route.post("/recipes")
async def create_recipe(data: _models.RecipeCreate, token: str = Depends(_service.get_authorization_header)):
    try:
        serialized_data = {"title": data.title, "description": data.description, "instructions": data.instructions}
        return await _service.processRequest(f"{BASE_URL}/recipes", 'POST', token=token, data=serialized_data)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@recipe_route.get("/recipes", tags=['Recipes Service'])
async def get_all_recipe(token: str = Depends(_service.get_authorization_header)):
    try:
        return await _service.processRequest(f"{BASE_URL}/recipes", 'GET', token=token)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@recipe_route.get("/recipes/{recipe_id}", tags=['Recipe Service'])
async def get_one_recipe(recipe_id: int, token: str = Depends(_service.get_authorization_header)):
    try:
        return await _service.processRequest(f"{BASE_URL}/recipes/{recipe_id}", 'GET', token=token)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    