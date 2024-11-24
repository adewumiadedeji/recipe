from fastapi import FastAPI, HTTPException ,  File, UploadFile
import fastapi as _fastapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from prometheus_client import make_asgi_app

import requests
import base64
import pika
import logging
import os
from jose import jwt
import rpc_client
import models as _models

from shared.middleware import AuthMiddleware, MetricsMiddleware


app = FastAPI(
    title="User Service",
    description="User management and authentication service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(AuthMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


logging.basicConfig(level=logging.INFO)

# Retrieve environment variables
JWT_SECRET = os.environ.get("JWT_SECRET")
AUTH_BASE_URL = os.environ.get("AUTH_BASE_URL")
RABBITMQ_URL = os.environ.get("RABBITMQ_URL") or "localhost"

# # Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.117.2')) # add container name in docker
channel = connection.channel()
channel.queue_declare(queue='gatewayservice')
channel.queue_declare(queue='authservice')


# JWT token validation
async def jwt_validation(token: str = _fastapi.Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")


@app.get("/")
async def home():
    return "You are welcome my buddy."

# Authentication routes
@app.get("/auth")
async def authService():
    try:
        response = requests.get(f"{AUTH_BASE_URL}/api/v1")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")

@app.post("/auth/login", tags=['Authentication Service'])
async def login(user_data: _models.UserCredentials):
    try:
        response = requests.post(f"{AUTH_BASE_URL}/api/v1/auth/token", json={"username": user_data.username, "password": user_data.password})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")

@app.post("/auth/register", tags=['Authentication Service'])
async def registeration(user_data: _models.UserRegisteration):
    
    try:
        response = requests.post(f"{os.getenv('HOST_SERVICE_HOST_URL')}/api/v1/auth/users", json={"name":user_data.name,"email": user_data.email, "password": user_data.password})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")

@app.post("/auth/generate_otp", tags=['Authentication Service'])
async def generate_otp(user_data: _models.GenerateOtp):
    try:
        response = requests.post(f"{os.getenv('HOST_SERVICE_HOST_URL')}/api/v1/auth/users/generate_otp", json={"email":user_data.email})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")

@app.post("/auth/verify_otp", tags=['Authentication Service'])
async def verify_otp(user_data: _models.VerifyOtp):
    try:
        response = requests.post(f"{os.getenv('HOST_SERVICE_HOST_URL')}/api/v1/auth/users/verify_otp", json={"email":user_data.email ,"otp":user_data.otp})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Authentication service is unavailable")



# ml microservice route - OCR route
@app.post('/ocr' ,  tags=['Machine learning Service'] )
def ocr(file: UploadFile = File(...),
        payload: dict = _fastapi.Depends(jwt_validation)):
    
    # Save the uploaded file to a temporary location
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    ocr_rpc = rpc_client.OcrRpcClient()

    with open(file.filename, "rb") as buffer:
        file_data = buffer.read()
        file_base64 = base64.b64encode(file_data).decode()
    
    request_json = {
        'user_name':payload['name'],
        'user_email':payload['email'],
        'user_id':payload['id'],
        'file': file_base64
    }

    # Call the OCR microservice with the request JSON
    response = ocr_rpc.call(request_json)

    # Delete the temporary image file
    os.remove(file.filename)
    return response