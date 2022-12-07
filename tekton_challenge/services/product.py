from dataclasses import dataclass
from typing import Iterator

from fastapi.logger import logger

from tekton_challenge.models.product import Product
from tekton_challenge.repositories.cache import CacheNotFound, CacheProtocol, TTLExpired
from tekton_challenge.repositories.product import ProductRepository
from tekton_challenge.schemas.product import ProductCreate, ProductUpdate


@dataclass
class ProductService:
    _repository: ProductRepository
    _cache_repository: CacheProtocol

    def get_products(self) -> Iterator[Product]:
        logger.info("Getting all products")
        products = self._repository.get_all()
        for product in products:
            self._set_status_name(product)
        return products

    def get_product_by_id(self, product_id: int) -> Product:
        logger.info(f"Getting product with id {product_id}")
        product = self._repository.get_by_id(product_id)
        self._set_status_name(product)
        return product

    def create_product(self, product: ProductCreate) -> Product:
        logger.info(f"Create a product: {product}")
        return self._repository.add(**product.dict())

    def update_product(self, product_id: int, product_update: ProductUpdate) -> None:
        logger.info(f"Update a product: {product_update}")
        return self._repository.update(product_id=product_id, **product_update.dict())

    def delete_product_by_id(self, product_id: int) -> None:
        logger.info(f"Create product: {product_id}")
        return self._repository.delete_by_id(product_id)

    def _get_cached_status_name(self, key: bool):
        try:
            return self._cache_repository.get(int(key))
        except (CacheNotFound, TTLExpired):
            self._set_cached_status_name(key)
            return self._cache_repository.get(int(key))

    def _set_status_name(self, product: Product):
        setattr(product, "status_name", self._get_cached_status_name(product.status))

    def _set_cached_status_name(self, key: bool):
        if key:
            return self._cache_repository.set(int(key), "Active")
        return self._cache_repository.set(int(key), "Inactive")
