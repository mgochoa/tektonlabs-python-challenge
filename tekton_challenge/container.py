from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from tekton_challenge.config.config import settings
from tekton_challenge.config.database import Database
from tekton_challenge.repositories.cache import LocalCacheRepository
from tekton_challenge.repositories.product import ProductRepository
from tekton_challenge.services.product import ProductService


class Container(DeclarativeContainer):
    db = Singleton(Database, db_url=settings.db_url)
    cache_repository = Singleton(LocalCacheRepository)

    wiring_config = WiringConfiguration(modules=[".routers.products"])

    products_repository = Factory(
        ProductRepository, db.provided.session
    )

    products_service = Factory(
        ProductService, products_repository, cache_repository
    )
