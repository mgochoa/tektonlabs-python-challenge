from unittest.mock import patch

import pytest
from requests import Session

from tekton_challenge.repositories.discount import ProductDiscount, ProductDiscountRepository


def discount_response():
    return {"discount": 12148, "id": "2"}


@pytest.fixture
def discount_repository():
    yield ProductDiscountRepository()


def mock_session_get_successful(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            return

    return MockResponse(discount_response(), 200)


@patch.object(Session, 'get', mock_session_get_successful)
def test_get_discount(discount_repository):
    response = discount_repository.get_discount()

    assert isinstance(response, ProductDiscount)
    assert response.value == 0.48
