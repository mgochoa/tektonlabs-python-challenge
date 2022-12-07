import pytest
from fastapi.testclient import TestClient

from tekton_challenge.main import app


@pytest.fixture
def http_client():
    yield TestClient(app)


@pytest.fixture
def create_product_body():
    yield {
        "name": "My Product",
        "status": 1,
        "description": "Test product",
        "price": 100,
        "discount": 0.5
    }


@pytest.fixture
def update_product_body(create_product_body):
    body = create_product_body
    body.update({"product_id": 1})
    return body
