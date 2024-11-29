from fastapi import FastAPI, HTTPException ,  File, UploadFile
import fastapi as _fastapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from prometheus_client import make_asgi_app


import base64
import pika
import logging
import os
from jose import jwt
import rpc_client

from utils.middleware import AuthMiddleware, MetricsMiddleware
from routes.auth import auth_route
from routes.ingredient import ing_route
from routes.mealplan import meal_route
from routes.recipe import recipe_route
from routes.rating import rate_route
from starlette.responses import RedirectResponse


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

RABBITMQ_URL = os.environ.get("RABBITMQ_URL") or "192.168.117.2"

# # Connect to RabbitMQ
# connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_URL)) # add container name in docker
# channel = connection.channel()
# channel.queue_declare(queue='gatewayservice')
# channel.queue_declare(queue='authservice')


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

@app.get("/docs")
async def docs():
    return RedirectResponse(url="/docs/")

# Authentication routes

app.include_router(auth_route, prefix='/api/v1', tags=['Auth'])
app.include_router(recipe_route, prefix='/api/v1', tags=['Recipe'])
app.include_router(ing_route, prefix='/api/v1', tags=['Ingredient'])
app.include_router(meal_route, prefix='/api/v1', tags=['Meal Plan'])
app.include_router(rate_route, prefix='/api/v1', tags=['Ratings'])


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