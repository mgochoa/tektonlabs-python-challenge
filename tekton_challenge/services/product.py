from dataclasses import dataclass
from typing import Iterator

from fastapi.logger import logger

from tekton_challenge.models.product import Product
from tekton_challenge.repositories.cache import CacheNotFound, CacheProtocol, TTLExpired
from tekton_challenge.repositories.discount import ProductDiscountRepository
from tekton_challenge.repositories.product import ProductRepository
from tekton_challenge.schemas.product import ProductCreate, ProductUpdate


@dataclass
class ProductService:
    """ Business logic for products"""
    _repository: ProductRepository
    _cache_repository: CacheProtocol
    _discount_repository: ProductDiscountRepository

    def get_products(self) -> Iterator[Product]:
        """
        Get all products, set the status name because it's a computed/derived field
        :return:
        """
        logger.info("Getting all products")
        products = self._repository.get_all()
        for product in products:
            self._set_status_name(product)
        return products

    def get_product_by_id(self, product_id: int) -> Product:
        """ Get a single product and set the status_name"""
        logger.info(f"Getting product with id {product_id}")
        product = self._repository.get_by_id(product_id)
        self._set_status_name(product)
        return product

    def create_product(self, product: ProductCreate) -> Product:
        """
        Get the product discount using an external service and create a new product in DB
        :param product:
        :return:
        """
        logger.info(f"Create a product: {product}")

        discount = self._discount_repository.get_discount()
        product.discount = discount.value
        db_product = self._repository.add(**product.dict())
        return db_product

    def update_product(self, product_id: int, product_update: ProductUpdate) -> None:
        logger.info(f"Update a product: {product_update}")
        return self._repository.update(product_id=product_id, **product_update.dict())

    def delete_product_by_id(self, product_id: int) -> None:
        logger.info(f"Create product: {product_id}")
        return self._repository.delete_by_id(product_id)

    def _get_cached_status_name(self, key: bool):
        """
        Gets the value of status_name using the status value, if it does not exist or it is expired then
        set a new value on the cache
        :param key:
        :return:
        """
        try:
            return self._cache_repository.get(int(key))
        except (CacheNotFound, TTLExpired):
            self._set_cached_status_name(key)
            return self._cache_repository.get(int(key))

    def _set_status_name(self, product: Product):
        """
        Set a status_name field in the product object, obtaining the status name from cache
        :param product: Product model
        :return:
        """
        setattr(product, "status_name", self._get_cached_status_name(product.status))

    def _set_cached_status_name(self, key: bool):
        """
        Set a status_name in the cache according to the key value
        :param key: it could be 1 or 0
        :return:
        """
        if key:
            return self._cache_repository.set(int(key), "Active")
        return self._cache_repository.set(int(key), "Inactive")
