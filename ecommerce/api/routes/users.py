from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ecommerce.core.database import get_session
from ecommerce.core.security import get_token_subject
from ecommerce.users.models import User
from ecommerce.users.repositories import UserRepository
from ecommerce.users.schemas import Message, UserRead, UserUpdate
from ecommerce.users.services import (
    EmailAlreadyExistsError,
    InvalidCurrentPasswordError,
    PasswordChangeValidationError,
    PhoneNumberAlreadyExistsError,
    UserNotFoundError,
    UserService,
)


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))


router = APIRouter(prefix='/users', tags=['users'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token/')


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> User:
    subject = get_token_subject(token)
    try:
        return service.get_user_by_email(subject)
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Could not validate credentials.',
        )


def validate_user_access(request_user_id: str, current_user: User) -> None:
    if request_user_id != current_user.public_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions.',
        )


@router.get(
    path='/me/{user_id}/',
    response_model=UserRead,
)
def read_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    validate_user_access(user_id, current_user)
    try:
        return service.get_user_by_public_id(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.',
        )


@router.put(
    path='/me/{user_id}/',
    response_model=UserRead,
)
def update_user(
    user_id: str,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    validate_user_access(user_id, current_user)
    try:
        return service.update_user(public_id=user_id, payload=user_update)
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.',
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
    except PasswordChangeValidationError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Both current_password and password are required '
                'to change password.'
            ),
        )
    except InvalidCurrentPasswordError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Current password is incorrect.',
        )


@router.delete(
    path='/me/{user_id}/',
    response_model=Message,
)
def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    validate_user_access(user_id, current_user)
    try:
        service.delete_user(public_id=user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.',
        )

    return {'message': 'User deleted.'}
