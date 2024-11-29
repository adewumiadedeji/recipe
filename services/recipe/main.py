from fastapi import FastAPI

from utils.database import engine, Base
import models as _models
import logging
from router import router
from prometheus_client import make_asgi_app


app = FastAPI(
    title="Recipe Service",
    description="Recipe management service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app = FastAPI()
logging.basicConfig(level=logging.INFO)


# Mount metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# @app.on_event("startup")
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(_models.Base.metadata.create_all)

# Create database tables
_models.Base.metadata.create_all(bind=engine)

    
app.include_router(router, prefix='/api/v1', tags=['recipe'])