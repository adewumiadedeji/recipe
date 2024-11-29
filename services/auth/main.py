import fastapi as _fastapi
from router import router
from utils.database import engine, Base
import logging
import models as _models


app = _fastapi.FastAPI()
logging.basicConfig(level=logging.INFO)


Base.metadata.create_all(bind=engine)

# for route in router.routes:
#     print(route)
    
app.include_router(router, prefix='/api/v1', tags=['users'])