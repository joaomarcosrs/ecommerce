import uuid
from http import HTTPStatus

from fastapi.testclient import TestClient


def test_create_user_success(
    client: TestClient,
    create_user
):

    user = create_user(
        name='John Doe',
        email='john.doe@example.com'
    )

    assert user['name'] == 'John Doe'
    assert user['email'] == 'john.doe@example.com'
    assert user['phone_number'] is None
    assert 'public_id' in user
    assert 'created_at' in user
    assert 'updated_at' in user


def test_create_user_conflict(
    client: TestClient,
    create_user
):
    user_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'secret',
        'phone_number': None
    }

    response1 = client.post('/users/', json=user_data)
    assert response1.status_code == HTTPStatus.CREATED

    response2 = client.post('/users/', json=user_data)
    assert response2.status_code == HTTPStatus.CONFLICT


def test_create_user_conflict_phone(
    client: TestClient,
    create_user
):
    create_user(
        name='Alice',
        email='alice@example.com',
        phone_number='1234567890'
    )

    user_data = {
        'name': 'Bob',
        'email': 'bob@example.com',
        'password': 'secret',
        'phone_number': '1234567890',
    }

    response = client.post('/users/', json=user_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Phone number already in use.'


def test_read_user_not_found(
    client: TestClient,
):
    fake_user_id = str(uuid.uuid4())

    response = client.get(
        url=f'/users/{fake_user_id}/',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found.'


def test_read_user(
    client: TestClient,
    create_user
):
    user = create_user(
        name='John Doe',
        email='john.doe@example.com'
    )
    response = client.get(
        url=f'/users/{user['public_id']}/',
    )
    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body['public_id'] == user['public_id']
    assert body['name'] == 'John Doe'
    assert body['email'] == 'john.doe@example.com'


def test_read_users(
    client: TestClient,
    create_user
):
    user1 = create_user(name='Alice', email='alice@example.com')
    user2 = create_user(name='Bob', email='bob@example.com')

    response = client.get('/users/', params={'skip': 0, 'limit': 10})
    assert response.status_code == HTTPStatus.OK

    body = response.json()
    emails = [u['email'] for u in body['users']]

    assert body['total'] == len([user1, user2])
    assert user1['email'] in emails
    assert user2['email'] in emails
