import pytest

pytestmark = pytest.mark.skip(
    reason='Domínio cart ainda não implementado no projeto.'
)


def test_add_product_to_cart_requires_authentication():
    raise NotImplementedError


def test_remove_product_from_cart_requires_authentication():
    raise NotImplementedError
