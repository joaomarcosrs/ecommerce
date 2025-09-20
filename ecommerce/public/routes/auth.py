from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from ecommerce.database import get_session
from ecommerce.public.models import User
from ecommerce.public.schemas import Token, UserCreate, UserRead
from ecommerce.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path='/register/',
    status_code=HTTPStatus.CREATED,
    response_model=UserRead
)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    if user.email:
        db_user_by_email = session.scalar(
            select(User).where(User.email == user.email)
        )
        if db_user_by_email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already in use.'
            )

    if user.phone_number:
        db_user_by_phone = session.scalar(
            select(User).where(User.phone_number == user.phone_number)
        )
        if db_user_by_phone:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Phone number already in use.'
            )

    db_user = User(
        email=user.email,
        phone_number=user.phone_number,
        name=user.name,
        password=get_password_hash(
            password=user.password
        )
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.post(
    path='/token/',
    response_model=Token
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(
            User.email == form_data.username
        )
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password.'
        )

    if not verify_password(
        plain_password=form_data.password,
        hashed_password=user.password
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password.'
        )

    access_token = create_access_token(
        data={
            'sub': user.email
        }
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
