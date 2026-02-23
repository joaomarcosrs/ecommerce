from fastapi import APIRouter

from ecommerce.api.routes import auth, products, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(users.router)
