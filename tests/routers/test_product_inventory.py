from unittest import mock

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, \
    HTTP_500_INTERNAL_SERVER_ERROR

from tekton_challenge.main import app
from tekton_challenge.models.product import Product
from tekton_challenge.repositories.cache import LocalCacheRepository
from tekton_challenge.repositories.errors import NotFoundError
from tekton_challenge.repositories.product import ProductRepository

# Mock cache repository
cache_repository_mock = mock.Mock(spec=LocalCacheRepository)
cache_repository_mock.get.return_value = "Active"
cache_repository_mock.set.return_value = None


def test_get_product_by_id(http_client):
    repository_mock = mock.Mock(spec=ProductRepository)
    repository_mock.get_by_id.return_value = Product(product_id=1, name="Product 1",
                                                     description="Description 1", status=1,
                                                     discount=0.1,
                                                     price=29.99)

    app.container.products_repository.override(repository_mock)
    app.container.cache_repository.override(cache_repository_mock)

    response = http_client.get("/inventory/products/1")

    assert response.status_code == HTTP_200_OK
    assert response.json().get("product_id") == 1
    assert response.json().get("price") == 29.99
    assert response.json().get("status_name") == "Active"


def test_get_product_by_id_not_found(http_client):
    repository_mock = mock.Mock(spec=ProductRepository)
    product_id_mock = 1
    repository_mock.get_by_id.side_effect = NotFoundError("Product", product_id_mock)

    app.container.products_repository.override(repository_mock)
    app.container.cache_repository.override(cache_repository_mock)
    response = http_client.get("/inventory/products/1")

    assert response.status_code == HTTP_404_NOT_FOUND


def test_get_product_by_id_server_error(http_client):
    repository_mock = mock.Mock(spec=ProductRepository)
    repository_mock.get_by_id.side_effect = Exception()

    app.container.products_repository.override(repository_mock)
    app.container.cache_repository.override(cache_repository_mock)
    response = http_client.get("/inventory/products/1")

    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_create_product(http_client):
    repository_mock = mock.Mock(spec=ProductRepository)
    product_mock = Product(product_id=1, name="Product 1",
                           description="Description 1", status=1,
                           discount=0.1,
                           price=29.99)
    repository_mock.add.return_value = product_mock
    body = {
        "name": product_mock.name,
        "price": product_mock.price,
        "description": product_mock.description,
        "status": product_mock.status,
        "discount": product_mock.discount
    }

    app.container.products_repository.override(repository_mock)
    app.container.cache_repository.override(cache_repository_mock)
    response = http_client.post("/inventory/products", json=body)

    assert response.status_code == HTTP_201_CREATED
    assert response.json().get("product_id") == 1
    assert repository_mock.add.called_once_with(**body)


def test_put_product(http_client, create_product_body):
    repository_mock = mock.Mock(spec=ProductRepository)
    repository_mock.update.return_value = None

    app.container.products_repository.override(repository_mock)
    app.container.cache_repository.override(cache_repository_mock)

    response = http_client.put("/inventory/products/1", json=create_product_body)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert repository_mock.update.called_once_with(product_id=1, **create_product_body)


def test_put_product_not_found(http_client, create_product_body):
    repository_mock = mock.Mock(spec=ProductRepository)
    product_id_mock = 1
    repository_mock.update.side_effect = NotFoundError("Product", product_id_mock)

    app.container.products_repository.override(repository_mock)
    app.container.cache_repository.override(cache_repository_mock)
    response = http_client.put(f"/inventory/products/{product_id_mock}", json=create_product_body)

    assert response.status_code == HTTP_404_NOT_FOUND
