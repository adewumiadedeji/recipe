from fastapi import FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from datetime import datetime, timedelta
import logging
from prometheus_client import Counter, Histogram
import time
import os

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "cfgcgkghj&*^^jhutbdrhgffrsrwaew@!srdhyjtuyiuyuiyyut76r65ty8u$#oun9y876r5r56r5")
ALGORITHM = os.getenv("ALGORITHM", 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 30)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(method=method, endpoint=path, status=400).inc()
            REQUEST_LATENCY.observe(duration)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude specific paths from validation if needed
        if request.url.path in ["/", "/api/v1/auth", "/api/v1/auth/login", "/api/v1/auth/register", "/docs/"]:
            return await call_next(request)

        # Extract the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

        token = auth_header.split(" ")[1]  # Extract the token
        
        try:
            # Validate and decode the token
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            # Add user info from the token to the request state
            request.state.user = payload
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.exceptions.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Proceed to the next middleware or endpoint
        response = await call_next(request)
        return response