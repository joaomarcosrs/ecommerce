from ecommerce.backend.core.db.base import table_registry
from ecommerce.backend.products import models as _product_models  # noqa: F401
from ecommerce.backend.users import models as _user_models  # noqa: F401

__all__ = ['table_registry']
