from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    status_name: str
    description: str
    price: float
    discount: int


class Product(ProductBase):
    product_id: int

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    status_name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    discount: Optional[int]
