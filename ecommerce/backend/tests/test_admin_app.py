import pytest

pytestmark = pytest.mark.skip(
    reason='Domínio admin ainda não implementado no projeto.'
)


def test_admin_can_create_product():
    raise NotImplementedError


def test_non_admin_cannot_create_product():
    raise NotImplementedError
