from sqlalchemy import Boolean, Column, Float, Integer, String

from tekton_challenge.config.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(Boolean)
    description = Column(String)
    price = Column(Float)
    discount = Column(Float)
