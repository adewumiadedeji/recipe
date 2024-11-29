from fastapi import FastAPI, HTTPException ,  Depends, APIRouter
import fastapi as _fastapi
import requests
import models as _models
import os
import service as _service

meal_route = APIRouter()

BASE_URL = os.environ.get("MEALPLAN_SERVICE_HOST_URL")


@meal_route.get("/meal-plan")
async def get_all_meals(token: str = Depends(_service.get_authorization_header)):
    try:
        return await _service.processRequest(f"{BASE_URL}/meal-plans", 'GET', token=token)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@meal_route.post("/meal-plan", tags=['Mealplan Service'])
async def create_meal(data: _models.MealCreate, token: str = Depends(_service.get_authorization_header)):
    try:
        serialized_data = {"date": data.date, "meal_type": data.meal_type.value, "recipe_id": data.recipe_id}
        return await _service.processRequest(f"{BASE_URL}/meal-plans", 'POST', token=token, data=serialized_data)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@meal_route.get("/meal-plan/{meal_id}", tags=['Mealplan Service'])
async def get_one_meal(meal_id: int, token: str = Depends(_service.get_authorization_header)):
    try:
        return await _service.processRequest(f"{BASE_URL}/meal-plans/{meal_id}", 'GET', token=token)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
