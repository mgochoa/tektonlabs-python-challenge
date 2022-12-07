from typing import Optional

from pydantic import BaseModel, validator


class ProductBase(BaseModel):
    """ Base to show in presentation layer"""
    name: str
    description: str
    price: float
    discount: float


class Product(ProductBase):
    """ Schema to show the products"""
    product_id: int
    final_price: Optional[float]
    status_name: Optional[str]

    @validator("final_price", always=True)
    def calculate_final_price(cls, v, values, **kwargs):
        return values["price"] - values["price"] * values["discount"]

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    """Schema to create a product"""
    name: str
    status: bool
    description: str
    price: float
    discount: Optional[float] = 0


class ProductUpdate(BaseModel):
    """Schema to update a product"""
    name: str
    status: int
    description: str
    price: float
    discount: Optional[float]
