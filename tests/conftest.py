from contextlib import contextmanager
from datetime import datetime
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from ecommerce.app import app
from ecommerce.database import get_session
from ecommerce.models import table_registry


@pytest.fixture
def client(session: Session) -> TestClient:
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine() -> Engine:
    return create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )


@pytest.fixture
def session(engine: Engine) -> Session:
    table_registry.metadata.drop_all(engine)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    event.listen(model, 'before_update', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)
    event.remove(model, 'before_update', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def create_user(client: TestClient):
    def _create_user(
        name='John Doe',
        email='john.doe@example.com',
        password='secret',
        phone_number=None,
    ):
        response = client.post(
            '/users/',
            json={
                'name': name,
                'email': email,
                'password': password,
                'phone_number': phone_number
            },
        )

        assert response.status_code == HTTPStatus.CREATED
        return response.json()

    return _create_user
