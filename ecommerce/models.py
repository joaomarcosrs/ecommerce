from ecommerce.core.db.base import table_registry
from ecommerce.products import models as _product_models  # noqa: F401
from ecommerce.users import models as _user_models  # noqa: F401

__all__ = ['table_registry']
