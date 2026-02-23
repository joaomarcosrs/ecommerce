import pytest
from fastapi import HTTPException
from jwt import decode
from jwt.exceptions import InvalidTokenError

from ecommerce.core import security
from ecommerce.core.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_token_subject,
)

STATUS_CODE_UNAUTHORIZED = 401


def test_jwt():
    data = {
        'test': 'test'
    }
    token = create_access_token(
        data=data
    )

    decoded = decode(
        jwt=token,
        key=SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token_subject():
    token = create_access_token(data={})

    with pytest.raises(
        HTTPException,
        match='Could not validate credentials.'
    ) as exc:
        get_token_subject(token)

    assert exc.value.status_code == STATUS_CODE_UNAUTHORIZED


def test_get_token_subject_invalid_token(monkeypatch):
    def mock_decode(*args, **kwargs):
        raise InvalidTokenError('Invalid token')

    monkeypatch.setattr(security, 'decode', mock_decode)

    with pytest.raises(
        HTTPException,
        match='Could not validate credentials.'
    ) as exc:
        get_token_subject('any-token')

    assert exc.value.status_code == STATUS_CODE_UNAUTHORIZED
