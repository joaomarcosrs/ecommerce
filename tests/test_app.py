from http import HTTPStatus

from fastapi.testclient import TestClient

from ecommerce.app import app
from ecommerce.schemas import UserRead

client = TestClient(app)


def test_create_user():
    response = client.post(
        url='/users',
        json={
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': '123456',
            'phone_number': None
        }
    )
    assert response.status_code == HTTPStatus.CREATED

    user = UserRead.model_validate(response.json())

    assert user.name == "John Doe"
    assert user.email == "john.doe@example.com"
    assert user.phone_number is None
    assert user.public_id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
