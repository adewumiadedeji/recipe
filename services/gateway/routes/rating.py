from fastapi import FastAPI, HTTPException , Depends, APIRouter
import fastapi as _fastapi
import requests
import models as _models
import os
import service as _service

rate_route = APIRouter()

BASE_URL = os.environ.get("RATING_SERVICE_HOST_URL")


@rate_route.post("/rates", tags=['Rating Service'])
async def create_rate(data: _models.RateCreate, token: str = Depends(_service.get_authorization_header)):
    try:
        serialized_data = {"recipe_id": data.recipe_id, "rate": data.rate}
        return await _service.processRequest(f"{BASE_URL}/rates", 'POST', token=token, data=serialized_data)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@rate_route.get("/rates/{recipe_id}", tags=['Rating Service'])
async def get_recipe_rate(recipe_id: int, token: str = Depends(_service.get_authorization_header)):
    try:
        return await _service.processRequest(f"{BASE_URL}/rates/{recipe_id}", 'GET', token=token)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    