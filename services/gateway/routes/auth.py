from fastapi import FastAPI, HTTPException ,  File, UploadFile, APIRouter, Depends
import fastapi as _fastapi
import requests
import models as _models
import os
import service as _service

auth_route = APIRouter()

BASE_URL = os.environ.get("AUTH_SERVICE_HOST_URL")


@auth_route.get("/auth")
async def authService():
    try:
        response = requests.get(f"{BASE_URL}/api/v1")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")

@auth_route.post("/auth/login", tags=['Authentication Service'])
async def login(user_data: _models.UserCredentials):
    try:
        return await _service.processRequest(f"{BASE_URL}/auth/token", 'POST', data={"email": user_data.email, "password": user_data.password})
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))

@auth_route.post("/auth/register", tags=['Authentication Service'])
async def registeration(user_data: _models.UserRegisteration):
    try:
        return await _service.processRequest(f"{BASE_URL}/users", 'POST', data={"name":user_data.name,"email": user_data.email, "password": user_data.password})
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    

@auth_route.post("/auth/generate-otp", tags=['Authentication Service'])
async def generate_otp(user_data: _models.GenerateOtp):
    try:
        return await _service.processRequest(f"{BASE_URL}/auth/generate-otp", 'POST', data={"email":user_data.email})
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    

@auth_route.post("/auth/verify-otp", tags=['Authentication Service'])
async def verify_otp(user_data: _models.VerifyOtp):
    try:
        return await _service.processRequest(f"{BASE_URL}/auth/verify-otp", 'POST', data={"email":user_data.email ,"otp":user_data.otp})
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    
@auth_route.get("/auth/profile")
async def getProfile(token: str = Depends(_service.get_authorization_header)):
    try:
        print("Token: ", token)
        return await _service.processRequest(f"{BASE_URL}/users/me", 'GET', token=token)
    except requests.exceptions.ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    