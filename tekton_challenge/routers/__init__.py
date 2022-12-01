from fastapi import APIRouter
from .product_inventory import router as product_router

inventory_router = APIRouter(
    prefix="/inventory"
)

inventory_router.include_router(product_router)
