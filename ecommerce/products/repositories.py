from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ecommerce.products.models import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_public_id(self, public_id: str) -> Product | None:
        return self.session.scalar(
            select(Product).where(Product.public_id == public_id)
        )

    def get_by_sku(self, sku: str) -> Product | None:
        return self.session.scalar(select(Product).where(Product.sku == sku))

    def get_all(self) -> list[Product]:
        return self.session.scalars(select(Product).order_by(Product.id)).all()

    def search(self, query: str) -> list[Product]:
        normalized_query = f'%{query.lower()}%'
        return self.session.scalars(
            select(Product)
            .where(
                or_(
                    func.lower(Product.name).like(normalized_query),
                    func.lower(Product.sku).like(normalized_query),
                )
            )
            .order_by(Product.created_at.desc())
        ).all()

    def create(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.commit()
