from dataclasses import dataclass

from sqlalchemy.orm import Session

from tekton_challenge.config.database import Base


@dataclass
class BaseDTO:
    """Base data transfer object service class"""
    db: Session

    def _commit(self, db_item: Base = None) -> None:
        """Commit the database transaction and refresh the item if there is one
        :param db_item: Item derived from the Base SQL Alchemy Model
        """
        self.db.commit()
        if db_item:
            self.db.refresh(db_item)
