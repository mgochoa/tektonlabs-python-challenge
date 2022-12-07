from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from tekton_challenge.main import app

client = TestClient(app)


def test_get_product_inventory_by_id():
    response = client.get("/inventory/products/1")
    assert response.status_code == HTTP_200_OK
    assert response.json().get("productId") == 1


def test_post_product_inventory():
    data = {}
    response = client.post("/inventory/products", json=data)
    assert response.status_code == HTTP_201_CREATED
    assert isinstance(response.headers.get("X-Location"), int)


def test_put_product_inventory():
    data = {"productId": 1}
    response = client.put(f"/inventory/products/{data['productId']}", json=data)
    assert response.status_code == HTTP_204_NO_CONTENT
