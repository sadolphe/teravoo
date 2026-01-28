from fastapi import APIRouter
from app.api.v1.endpoints import auth, products, orders, sourcing, producers, traceability, pricing

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(sourcing.router, prefix="/requests", tags=["sourcing"])
api_router.include_router(producers.router, prefix="/producers", tags=["producers"])
api_router.include_router(traceability.router, prefix="/traceability", tags=["traceability"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
