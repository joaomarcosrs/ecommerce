import pytest

pytestmark = pytest.mark.skip(
    reason='Domínio checkout ainda não implementado no projeto.'
)


def test_checkout_requires_authenticated_user():
    raise NotImplementedError


def test_checkout_without_items_returns_error():
    raise NotImplementedError
