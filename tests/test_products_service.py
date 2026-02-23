from unittest.mock import Mock

import pytest

from ecommerce.products.services import ProductNotFoundError, ProductService


def test_get_product_by_sku_success():
    product = object()
    repo = Mock()
    repo.get_by_sku.return_value = product
    service = ProductService(repo=repo)

    result = service.get_product_by_sku('sku-123')

    assert result is product
    repo.get_by_sku.assert_called_once_with('sku-123')


def test_get_product_by_sku_not_found():
    repo = Mock()
    repo.get_by_sku.return_value = None
    service = ProductService(repo=repo)

    with pytest.raises(ProductNotFoundError):
        service.get_product_by_sku('missing-sku')

    repo.get_by_sku.assert_called_once_with('missing-sku')
