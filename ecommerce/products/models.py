from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ecommerce.core.db.base import table_registry
from ecommerce.core.utils.ids import generate_public_id


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        init=False,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    price: Mapped[float] = mapped_column(
        nullable=False
    )
    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        init=False,
    )
    public_id: Mapped[str] = mapped_column(
        String(26),
        nullable=False,
        default_factory=generate_public_id,
    )
