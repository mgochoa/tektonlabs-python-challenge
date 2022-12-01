from fastapi import APIRouter, Depends

from tekton_challenge.config.database import get_db
from tekton_challenge.schemas.product import ProductCreate, Product

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(product_id: int, db: get_db = Depends()):
    pass


@router.post("/")
async def create_product(product_inventory: ProductCreate, db: get_db = Depends()):
    pass


@router.put("/{product_id}")
async def update_product(product_id: int):
    pass
