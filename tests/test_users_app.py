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

    response1 = client.post('/auth/register/', json=user_data)
    assert response1.status_code == HTTPStatus.CREATED

    response2 = client.post('/auth/register/', json=user_data)
    assert response2.status_code == HTTPStatus.CONFLICT
    assert response2.json()['detail'] == 'Email already in use.'


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

    response = client.post('/auth/register/', json=user_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Phone number already in use.'


def test_read_user_not_found(
    client: TestClient,
):
    fake_user_id = str(uuid.uuid4())

    response = client.get(
        url=f'/auth/me/{fake_user_id}/',
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
        url=f'/auth/me/{user['public_id']}/',
    )
    assert response.status_code == HTTPStatus.OK

    body = response.json()
    assert body['public_id'] == user['public_id']
    assert body['name'] == 'John Doe'
    assert body['email'] == 'john.doe@example.com'


def test_update_user_success(
    client: TestClient,
    create_user
):
    user = create_user(
        name='John Doe',
        email='john.doe@example.com',
        phone_number='1234567890'
    )

    update_data = {
        'name': 'John Updated',
        'email': 'john.updated@example.com'
    }

    response = client.put(
        f'/auth/me/{user["public_id"]}/',
        json=update_data
    )

    assert response.status_code == HTTPStatus.OK

    updated_user = response.json()
    assert updated_user['name'] == 'John Updated'
    assert updated_user['email'] == 'john.updated@example.com'
    assert updated_user['phone_number'] == '1234567890'
    assert updated_user['public_id'] == user['public_id']


def test_update_user_partial(
    client: TestClient,
    create_user
):
    user = create_user(
        name='John Doe',
        email='john.doe@example.com',
        phone_number='1234567890'
    )

    update_data = {
        'name': 'John Updated'
    }

    response = client.put(
        f'/auth/me/{user["public_id"]}/',
        json=update_data
    )

    assert response.status_code == HTTPStatus.OK

    updated_user = response.json()
    assert updated_user['name'] == 'John Updated'
    assert updated_user['email'] == 'john.doe@example.com'
    assert updated_user['phone_number'] == '1234567890'


def test_update_user_not_found(
    client: TestClient
):
    fake_user_id = str(uuid.uuid4())

    update_data = {
        'name': 'John Updated'
    }

    response = client.put(
        f'/auth/me/{fake_user_id}/',
        json=update_data
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found.'


def test_update_user_email_conflict(
    client: TestClient,
    create_user
):
    user1 = create_user(
        name='John Doe',
        email='john.doe@example.com'
    )

    create_user(
        name='Jane Doe',
        email='jane.doe@example.com'
    )

    update_data = {
        'email': 'jane.doe@example.com'
    }

    response = client.put(
        f'/auth/me/{user1["public_id"]}/',
        json=update_data
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Email already in use.'


def test_update_user_phone_conflict(
    client: TestClient,
    create_user
):
    user1 = create_user(
        name='John Doe',
        email='john.doe@example.com',
        phone_number='1234567890'
    )

    create_user(
        name='Jane Doe',
        email='jane.doe@example.com',
        phone_number='9876543210'
    )

    update_data = {
        'phone_number': '9876543210'
    }

    response = client.put(
        f'/auth/me/{user1["public_id"]}/',
        json=update_data
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Phone number already in use.'


def test_update_user_same_email(
    client: TestClient,
    create_user
):
    user = create_user(
        name='John Doe',
        email='john.doe@example.com'
    )

    update_data = {
        'name': 'John Updated',
        'email': 'john.doe@example.com'
    }

    response = client.put(
        f'/auth/me/{user["public_id"]}/',
        json=update_data
    )

    assert response.status_code == HTTPStatus.OK

    updated_user = response.json()
    assert updated_user['name'] == 'John Updated'
    assert updated_user['email'] == 'john.doe@example.com'


def test_update_user_same_phone(
    client: TestClient,
    create_user
):
    user = create_user(
        name='John Doe',
        email='john.doe@example.com',
        phone_number='1234567890'
    )

    update_data = {
        'name': 'John Updated',
        'phone_number': '1234567890'
    }

    response = client.put(
        f'/auth/me/{user["public_id"]}/',
        json=update_data
    )

    assert response.status_code == HTTPStatus.OK

    updated_user = response.json()
    assert updated_user['name'] == 'John Updated'
    assert updated_user['phone_number'] == '1234567890'


def test_update_user_password(
    client: TestClient,
    create_user
):
    user = create_user(
        name='John Doe',
        email='john.doe@example.com',
        password='old_password'
    )

    update_data = {
        'password': 'new_password'
    }

    response = client.put(
        f'/auth/me/{user["public_id"]}/',
        json=update_data
    )

    assert response.status_code == HTTPStatus.OK

    updated_user = response.json()
    assert updated_user['name'] == 'John Doe'
    assert updated_user['email'] == 'john.doe@example.com'


def test_delete_user_success(
    client: TestClient,
    create_user
):
    user = create_user(
        name='John Doe',
        email='john.doe@example.com'
    )

    response = client.delete(f'/auth/me/{user["public_id"]}/')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b''


def test_delete_user_not_found(
    client: TestClient
):
    fake_user_id = str(uuid.uuid4())

    response = client.delete(f'/auth/me/{fake_user_id}/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found.'


def test_delete_user_verify_deletion(
    client: TestClient,
    create_user
):
    user = create_user(
        name='John Doe',
        email='john.doe@example.com'
    )

    delete_response = client.delete(f'/auth/me/{user["public_id"]}/')
    assert delete_response.status_code == HTTPStatus.NO_CONTENT

    get_response = client.get(f'/auth/me/{user["public_id"]}/')
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_response.json()['detail'] == 'User not found.'
