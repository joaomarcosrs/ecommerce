from ecommerce.products.models import Product
from ecommerce.products.repositories import ProductRepository
from ecommerce.products.schemas import ProductUpdate


class SKUAlreadyExistsError(Exception): ...


class ProductNotFoundError(Exception): ...


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(
        self,
        *,
        name: str,
        description: str | None = None,
        price: float,
        sku: str,
    ) -> Product:
        if self.repo.get_by_sku(sku):
            raise SKUAlreadyExistsError()

        product = Product(
            name=name,
            description=description,
            price=price,
            sku=sku,
        )
        return self.repo.create(product)

    def get_product_by_public_id(self, public_id: str) -> Product:
        product = self.repo.get_by_public_id(public_id)
        if not product:
            raise ProductNotFoundError()
        return product

    def get_product_by_sku(self, sku: str) -> Product:
        product = self.repo.get_by_sku(sku)
        if not product:
            raise ProductNotFoundError()
        return product

    def list_products(self, query: str | None = None) -> list[Product]:
        if query:
            return self.repo.search(query)
        return self.repo.get_all()

    def update_product(
        self,
        *,
        public_id: str,
        payload: ProductUpdate,
    ) -> Product:
        product = self.get_product_by_public_id(public_id)

        if payload.sku and payload.sku != product.sku and self.repo.get_by_sku(
            payload.sku
        ):
            raise SKUAlreadyExistsError()

        update_data = payload.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        return self.repo.update(product)

    def delete_product(self, *, public_id: str) -> None:
        product = self.get_product_by_public_id(public_id)
        self.repo.delete(product)
