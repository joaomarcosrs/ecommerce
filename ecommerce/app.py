from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ecommerce.database import get_session
from ecommerce.models import User
from ecommerce.schemas import UserRead, UserSchema, UserUpdate
from ecommerce.security import get_password_hash, verify_password

app = FastAPI()


@app.post(
    path='/auth/register/',
    status_code=HTTPStatus.CREATED,
    response_model=UserRead
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
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


@app.get(
    path='/auth/me/{user_id}/',
    response_model=UserRead
)
def read_user(user_id: str, session: Session = Depends(get_session)):
    user = session.scalar(
        select(User).where(
            User.public_id == user_id
        )
    )
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.'
        )

    return user


@app.put(
    path='/auth/me/{user_id}/',
    response_model=UserRead
)
def update_user(
    user_id: str,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
):

    db_user = session.scalar(
        select(User).where(User.public_id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.'
        )

    if user_update.email and user_update.email != db_user.email:
        existing_user = session.scalar(
            select(User).where(User.email == user_update.email)
        )
        if existing_user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already in use.'
            )

    if user_update.phone_number and \
        user_update.phone_number != db_user.phone_number:

        existing_user = session.scalar(
            select(User).where(User.phone_number == user_update.phone_number)
        )
        if existing_user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Phone number already in use.'
            )

    has_password_fields = (
        user_update.password is not None or
        user_update.current_password is not None
    )
    if has_password_fields:
        if not user_update.current_password or not user_update.password:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=(
                    'Both current_password and password are required '
                    'to change password.'
                )
            )

        if not verify_password(
            plain_password=user_update.current_password,
            hashed_password=db_user.password
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Current password is incorrect.'
            )

        user_update.password = get_password_hash(
            password=user_update.password
        )
    else:
        # Se não há campos de senha, remover do update_data
        user_update.current_password = None
        user_update.password = None

    update_data = user_update.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete(
    path='/auth/me/{user_id}/',
    status_code=HTTPStatus.NO_CONTENT
)
def delete_user(
    user_id: str,
    session: Session = Depends(get_session)
):
    db_user = session.scalar(
        select(User).where(User.public_id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found.'
        )

    session.delete(db_user)
    session.commit()
