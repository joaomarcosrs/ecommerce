from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ecommerce.auth.schemas import Token
from ecommerce.core.database import get_session
from ecommerce.core.security import create_access_token
from ecommerce.users.repositories import UserRepository
from ecommerce.users.schemas import UserCreate, UserRead
from ecommerce.users.services import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    PhoneNumberAlreadyExistsError,
    UserService,
)

router = APIRouter(prefix='/auth', tags=['auth'])


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))


@router.post(
    path='/register/',
    status_code=HTTPStatus.CREATED,
    response_model=UserRead,
)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return service.create_user(
            email=user.email,
            phone_number=user.phone_number,
            name=user.name,
            password=user.password,
        )
    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Email already in use.',
        )
    except PhoneNumberAlreadyExistsError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Phone number already in use.',
        )


@router.post(
    path='/token/',
    response_model=Token,
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    try:
        user = service.authenticate(
            email=form_data.username,
            password=form_data.password,
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password.',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }
