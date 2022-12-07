from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from tekton_challenge.models.product import Product
from tekton_challenge.repositories.errors import NotFoundError


def raise_not_found(product_id: int):
    """Raise NotFoundError for Product Repository"""
    raise NotFoundError("Product", product_id)


@dataclass
class ProductRepository:
    session_factory: Callable[..., AbstractContextManager[Session]]

    def get_all(self) -> Iterator[Product]:
        """ Get all products"""
        with self.session_factory() as session:
            return session.query(Product).all()

    def get_by_id(self, product_id: int) -> Product:
        """Get one product"""
        with self.session_factory() as session:
            product = session.query(Product).filter(Product.product_id == product_id).first()
            if not product:
                raise_not_found(product_id)
            return product

    def add(self, *, name: str, status_name: str, description: str, price: float, discount: float) -> Product:
        with self.session_factory() as session:
            """Add a new product"""
            product = Product(name=name, status_name=status_name, description=description, price=price,
                              discount=discount)
            session.add(product)
            session.commit()
            session.refresh(product)
            return product

    def delete_by_id(self, product_id: int) -> None:
        """Delete a product"""
        with self.session_factory() as session:
            product: Product = session.query(Product).filter(Product.product_id == product_id).first()
            if not product:
                raise_not_found(product_id)
            session.delete(product)
            session.commit()

    def update(self, product_id: int, **kwargs):
        """ Update a product """
        with self.session_factory() as session:
            product: Product = session.query(Product).filter(Product.product_id == product_id).first()
            if not product:
                raise_not_found(product_id)

            for var, value in kwargs.items():
                setattr(product, var, value)
            session.add(product)
            session.commit()
            session.refresh(product)
