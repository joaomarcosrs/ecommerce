from unittest.mock import Mock

import pytest

from ecommerce.users.services import UserNotFoundError, UserService


def test_get_user_by_public_id_success():
    user = object()
    repo = Mock()
    repo.get_by_public_id.return_value = user
    service = UserService(repo=repo)

    result = service.get_user_by_public_id('public-id-123')

    assert result is user
    repo.get_by_public_id.assert_called_once_with('public-id-123')


def test_get_user_by_public_id_not_found():
    repo = Mock()
    repo.get_by_public_id.return_value = None
    service = UserService(repo=repo)

    with pytest.raises(UserNotFoundError):
        service.get_user_by_public_id('missing-id')

    repo.get_by_public_id.assert_called_once_with('missing-id')
