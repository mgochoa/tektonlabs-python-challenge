from typing import Optional

from pydantic import BaseModel, validator


class ProductBase(BaseModel):
    name: str
    status_name: str
    description: str
    price: float
    discount: float


class Product(ProductBase):
    product_id: int
    final_price: Optional[float]

    @validator("final_price", always=True)
    def calculate_final_price(cls, v, values, **kwargs):
        return values["price"] - values["price"] * values["discount"]

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str
    status_name: str
    description: str
    price: float
    discount: float
