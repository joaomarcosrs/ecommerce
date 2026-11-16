import uuid
from http import HTTPStatus

from fastapi.testclient import TestClient

KEYBOARD_PRICE = 499.9
KEYBOARD_PRO_PRICE = 599.9
MOUSE_PRICE = 199.9
EXPECTED_PRODUCT_COUNT = 2


def test_create_product_success(client: TestClient):
    response = client.post(
        '/products/',
        json={
            'name': 'Keyboard',
            'description': 'Mechanical keyboard',
            'price': KEYBOARD_PRICE,
            'sku': 'KEY-001',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert body['name'] == 'Keyboard'
    assert body['sku'] == 'KEY-001'
    assert body['price'] == KEYBOARD_PRICE
    assert 'public_id' in body


def test_create_product_conflict_sku(client: TestClient):
    payload = {
        'name': 'Keyboard',
        'description': 'Mechanical keyboard',
        'price': KEYBOARD_PRICE,
        'sku': 'KEY-001',
    }

    first = client.post('/products/', json=payload)
    second = client.post('/products/', json=payload)

    assert first.status_code == HTTPStatus.CREATED
    assert second.status_code == HTTPStatus.CONFLICT
    assert second.json()['detail'] == 'SKU already in use.'


def test_list_products(client: TestClient):
    client.post(
        '/products/',
        json={
            'name': 'Keyboard',
            'description': 'Mechanical keyboard',
            'price': KEYBOARD_PRICE,
            'sku': 'KEY-001',
        },
    )
    client.post(
        '/products/',
        json={
            'name': 'Mouse',
            'description': 'Wireless mouse',
            'price': MOUSE_PRICE,
            'sku': 'MOU-001',
        },
    )

    response = client.get('/products/')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == EXPECTED_PRODUCT_COUNT


def test_search_products(client: TestClient):
    client.post(
        '/products/',
        json={
            'name': 'Keyboard',
            'description': 'Mechanical keyboard',
            'price': KEYBOARD_PRICE,
            'sku': 'KEY-001',
        },
    )
    client.post(
        '/products/',
        json={
            'name': 'Mouse',
            'description': 'Wireless mouse',
            'price': MOUSE_PRICE,
            'sku': 'MOU-001',
        },
    )

    response = client.get('/products/?q=key')

    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert len(body) == 1
    assert body[0]['sku'] == 'KEY-001'


def test_get_product_by_public_id(client: TestClient):
    create_response = client.post(
        '/products/',
        json={
            'name': 'Keyboard',
            'description': 'Mechanical keyboard',
            'price': KEYBOARD_PRICE,
            'sku': 'KEY-001',
        },
    )
    product_id = create_response.json()['public_id']

    response = client.get(f'/products/{product_id}/')

    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body['public_id'] == product_id
    assert body['name'] == 'Keyboard'


def test_get_product_not_found(client: TestClient):
    fake_id = str(uuid.uuid4())

    response = client.get(f'/products/{fake_id}/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found.'


def test_update_product_success(client: TestClient):
    create_response = client.post(
        '/products/',
        json={
            'name': 'Keyboard',
            'description': 'Mechanical keyboard',
            'price': KEYBOARD_PRICE,
            'sku': 'KEY-001',
        },
    )
    product_id = create_response.json()['public_id']

    response = client.put(
        f'/products/{product_id}/',
        json={
            'name': 'Keyboard Pro',
            'price': KEYBOARD_PRO_PRICE,
        },
    )

    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body['name'] == 'Keyboard Pro'
    assert body['price'] == KEYBOARD_PRO_PRICE
    assert body['sku'] == 'KEY-001'


def test_update_product_conflict_sku(client: TestClient):
    first = client.post(
        '/products/',
        json={
            'name': 'Keyboard',
            'description': 'Mechanical keyboard',
            'price': KEYBOARD_PRICE,
            'sku': 'KEY-001',
        },
    )
    client.post(
        '/products/',
        json={
            'name': 'Mouse',
            'description': 'Wireless mouse',
            'price': MOUSE_PRICE,
            'sku': 'MOU-001',
        },
    )

    product_id = first.json()['public_id']
    response = client.put(
        f'/products/{product_id}/',
        json={
            'sku': 'MOU-001',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'SKU already in use.'


def test_update_product_not_found(client: TestClient):
    fake_id = str(uuid.uuid4())

    response = client.put(
        f'/products/{fake_id}/',
        json={
            'name': 'Non-existent Product',
            'price': 999.99,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found.'


def test_delete_product_success(client: TestClient):
    create_response = client.post(
        '/products/',
        json={
            'name': 'Keyboard',
            'description': 'Mechanical keyboard',
            'price': KEYBOARD_PRICE,
            'sku': 'KEY-001',
        },
    )
    product_id = create_response.json()['public_id']

    response = client.delete(f'/products/{product_id}/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Product deleted.'}


def test_delete_product_not_found(client: TestClient):
    fake_id = str(uuid.uuid4())

    response = client.delete(f'/products/{fake_id}/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found.'
