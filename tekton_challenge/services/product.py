from dataclasses import dataclass
from typing import Iterator

from fastapi.logger import logger

from tekton_challenge.models.product import Product
from tekton_challenge.repositories.product import ProductRepository
from tekton_challenge.schemas.product import ProductCreate, ProductUpdate


@dataclass
class ProductService:
    _repository: ProductRepository

    def get_products(self) -> Iterator[Product]:
        logger.info("Getting all products")
        return self._repository.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        logger.info(f"Getting product with id {product_id}")
        return self._repository.get_by_id(product_id)

    def create_product(self, product: ProductCreate) -> Product:
        logger.info(f"Create a product: {product}")
        return self._repository.add(**product.dict())

    def update_product(self, product_id: int, product_update: ProductUpdate) -> None:
        logger.info(f"Update a product: {product_update}")
        return self._repository.update(id=product_id, **product_update.dict())

    def delete_product_by_id(self, product_id: int) -> None:
        logger.info(f"Create product: {product_id}")
        return self._repository.delete_by_id(product_id)
