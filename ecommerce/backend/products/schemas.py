from datetime import datetime

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    sku: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    sku: str | None = None


class ProductRead(ProductBase):
    public_id: str
    created_at: datetime
    updated_at: datetime
