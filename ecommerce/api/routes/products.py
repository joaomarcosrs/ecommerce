from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ecommerce.core.database import get_session
from ecommerce.core.utils.schemas import Message
from ecommerce.products.repositories import ProductRepository
from ecommerce.products.schemas import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
)
from ecommerce.products.services import (
    ProductNotFoundError,
    ProductService,
    SKUAlreadyExistsError,
)

router = APIRouter(prefix='/products', tags=['products'])


def get_product_service(
    session: Session = Depends(get_session),
) -> ProductService:
    return ProductService(ProductRepository(session))


@router.post(
    path='/',
    status_code=HTTPStatus.CREATED,
    response_model=ProductRead,
)
def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.create_product(
            name=payload.name,
            description=payload.description,
            price=payload.price,
            sku=payload.sku,
        )
    except SKUAlreadyExistsError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='SKU already in use.',
        )


@router.get(
    path='/',
    response_model=list[ProductRead],
)
def list_products(
    q: str | None = Query(default=None, min_length=1),
    service: ProductService = Depends(get_product_service),
):
    return service.list_products(query=q)


@router.get(
    path='/{product_id}/',
    response_model=ProductRead,
)
def get_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.get_product_by_public_id(product_id)
    except ProductNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found.',
        )


@router.put(
    path='/{product_id}/',
    response_model=ProductRead,
)
def update_product(
    product_id: str,
    payload: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.update_product(public_id=product_id, payload=payload)
    except ProductNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found.',
        )
    except SKUAlreadyExistsError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='SKU already in use.',
        )


@router.delete(
    path='/{product_id}/',
    response_model=Message,
)
def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service),
):
    try:
        service.delete_product(public_id=product_id)
    except ProductNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found.',
        )

    return {'message': 'Product deleted.'}
