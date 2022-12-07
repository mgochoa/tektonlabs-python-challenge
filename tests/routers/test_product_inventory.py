from unittest import mock

import pytest
from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, \
    HTTP_500_INTERNAL_SERVER_ERROR

from tekton_challenge.main import app
from tekton_challenge.models.product import Product
from tekton_challenge.repositories.errors import NotFoundError
from tekton_challenge.repositories.product import ProductRepository


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_product_by_id(client):
    repository_mock = mock.Mock(spec=ProductRepository)
    repository_mock.get_by_id.return_value = Product(product_id=1, name="Product 1",
                                                     description="Description 1", status_name="active",
                                                     discount=0.1,
                                                     price=29.99)

    with app.container.products_repository.override(repository_mock):
        response = client.get("/inventory/products/1")

    assert response.status_code == HTTP_200_OK
    assert response.json().get("product_id") == 1
    assert response.json().get("price") == 29.99


def test_get_product_by_id_not_found(client):
    repository_mock = mock.Mock(spec=ProductRepository)
    product_id_mock = 1
    repository_mock.get_by_id.side_effect = NotFoundError("Product", product_id_mock)

    with app.container.products_repository.override(repository_mock):
        response = client.get("/inventory/products/1")

    assert response.status_code == HTTP_404_NOT_FOUND


def test_get_product_by_id_server_error(client):
    repository_mock = mock.Mock(spec=ProductRepository)
    repository_mock.get_by_id.side_effect = Exception()

    with app.container.products_repository.override(repository_mock):
        response = client.get("/inventory/products/1")

    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_create_product(client):
    repository_mock = mock.Mock(spec=ProductRepository)
    product_mock = Product(product_id=1, name="Product 1",
                           description="Description 1", status_name="active",
                           discount=0.1,
                           price=29.99)
    repository_mock.add.return_value = product_mock
    body = {
        "name": product_mock.name,
        "price": product_mock.price,
        "description": product_mock.description,
        "status_name": product_mock.status_name,
        "discount": product_mock.discount
    }

    with app.container.products_repository.override(repository_mock):
        response = client.post("/inventory/products", json=body)

    assert response.status_code == HTTP_201_CREATED
    assert response.json().get("product_id") == 1
    assert repository_mock.add.called_once_with(**body)


def test_put_product(client):
    repository_mock = mock.Mock(spec=ProductRepository)
    repository_mock.update.return_value = None

    body = {
        "name": "My Product",
        "status_name": "active",
        "description": "Test product",
        "price": 100,
        "discount": 0.5
    }

    with app.container.products_repository.override(repository_mock):
        response = client.put("/inventory/products/1", json=body)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert repository_mock.update.called_once_with(product_id=1, **body)


def test_put_product_not_found(client):
    repository_mock = mock.Mock(spec=ProductRepository)
    product_id_mock = 1
    repository_mock.update.side_effect = NotFoundError("Product", product_id_mock)

    body = {
        "name": "My Product",
        "status_name": "active",
        "description": "Test product",
        "price": 100,
        "discount": 0.5
    }
    with app.container.products_repository.override(repository_mock):
        response = client.put("/inventory/products/1", json=body)
    assert response.status_code == HTTP_404_NOT_FOUND
