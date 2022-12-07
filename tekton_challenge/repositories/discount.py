import logging
import random
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, validator
from requests import Session

from tekton_challenge.config.config import settings

logger = logging.getLogger(__name__)


class ProductDiscount(BaseModel):
    raw_discount: int
    value: Optional[float]

    @validator("value", always=True)
    def extract_discount(cls, v, values, **kwargs):
        return values["raw_discount"] % 100 / 100


@dataclass
class HttpRepository:
    """ Base http repository using requests"""
    url: str
    _session: Session = None

    @property
    def session(self) -> Session:
        if not self._session:
            self._session = Session()

        return self._session


@dataclass
class ProductDiscountRepository(HttpRepository):
    url: str = settings.discount_api_url

    def get_discount(self) -> ProductDiscount:
        random_product = random.randint(1, 100)
        query = f"{self.url}/products/{random_product}"

        logger.info(f"GET discount at {query}")

        response = self.session.get(query)
        response.raise_for_status()
        data = response.json()
        return ProductDiscount(raw_discount=data["discount"])
