from fastapi import FastAPI

from ecommerce.backend.api import api_router

app = FastAPI()

app.include_router(api_router)
