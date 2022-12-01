from dataclasses import dataclass

from tekton_challenge.models.product import Product as ProductInventoryModel
from tekton_challenge.schemas.product import Product as ProductInventorySchema
from tekton_challenge.services.base.dto import BaseDTO


@dataclass
class ProductInventoryService(BaseDTO):
    def get_product_inventory(self, product_id: int):
        return self.db.query(ProductInventoryModel).filter(ProductInventoryModel.product_id == product_id).first()

    def create_product_inventory(self, product_inventory: ProductInventorySchema):
        db_product_inventory = ProductInventoryModel(product_inventory)
        self.db.add(db_product_inventory)
        self._commit(db_product_inventory)
        return db_product_inventory

    def update_product_inventory(self, product: ProductInventorySchema):
        pass
