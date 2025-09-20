from http import HTTPStatus

from fastapi.testclient import TestClient


def test_create_token_for_access_success(
    client: TestClient,
    create_user
):

    password = 'secret'

    user = create_user(
        name='John Doe',
        email='john.doe@example.com',
        password=password
    )

    response = client.post(
        url='/token/',
        data={
            'username': user['email'],
            'password': password
        }
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_create_token_for_access_unauthorized(
    client: TestClient,
    create_user
):
    password = 'secret'

    user = create_user(
        name='John Doe',
        email='john.doe@example.com',
        password='secret'
    )

    response = client.post(
        url='/token/',
        data={
            'username': user['email'],
            'password': 'wrong_password'
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect email or password.'

    response2 = client.post(
        url='/token/',
        data={
            'username': 'wrong_email@example.com',
            'password': password
        }
    )

    assert response2.status_code == HTTPStatus.UNAUTHORIZED
    assert response2.json()['detail'] == 'Incorrect email or password.'
