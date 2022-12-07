from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends

from tekton_challenge.container import Container
from tekton_challenge.routers.decorators import error_handler
from tekton_challenge.schemas.product import ProductCreate, ProductUpdate
from tekton_challenge.services.product import ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("")
@inject
def get_products(
        product_service: ProductService = Depends(Provide[Container.products_service])):
    return product_service.get_products()


@router.get("/{product_id}")
@inject
@error_handler
def get_product_by_id(product_id: int,
                      product_service: ProductService = Depends(Provide[Container.products_service])):
    return product_service.get_product_by_id(product_id)


@router.post("")
@inject
def create_product(product: ProductCreate = Body(...),
                   product_service: ProductService = Depends(Provide[Container.products_service])):
    return product_service.create_product(product)


@router.put("/{product_id}")
@inject
@error_handler
def update_product(product_id: int, product: ProductUpdate = Body(...),
                   product_service: ProductService = Depends(Provide[Container.products_service])):
    return product_service.update_product(product_id, product)
