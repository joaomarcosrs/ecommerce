from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ecommerce.database import get_session
from ecommerce.models import User
from ecommerce.schemas import UserList, UserRead, UserSchema, UserUpdate

app = FastAPI()


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserRead)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    if user.email:
        db_user_by_email = session.scalar(
            select(User).where(User.email == user.email)
        )
        if db_user_by_email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already in use."
            )

    if user.phone_number:
        db_user_by_phone = session.scalar(
            select(User).where(User.phone_number == user.phone_number)
        )
        if db_user_by_phone:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Phone number already in use."
            )

    db_user = User(
        email=user.email,
        phone_number=user.phone_number,
        name=user.name,
        password=user.password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/{user_id}/', response_model=UserRead)
def read_user(user_id: str, session: Session = Depends(get_session)):
    user = session.scalar(
        select(User).where(
            User.public_id == user_id
        )
    )
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )

    return user


@app.put('/users/{user_id}/', response_model=UserRead)
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
            detail="User not found."
        )

    if user_update.email and user_update.email != db_user.email:
        existing_user = session.scalar(
            select(User).where(User.email == user_update.email)
        )
        if existing_user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already in use."
            )

    if user_update.phone_number and \
        user_update.phone_number != db_user.phone_number:

        existing_user = session.scalar(
            select(User).where(User.phone_number == user_update.phone_number)
        )
        if existing_user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Phone number already in use."
            )

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}/', status_code=HTTPStatus.NO_CONTENT)
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
            detail="User not found."
        )

    session.delete(db_user)
    session.commit()


@app.get('/users/', response_model=UserList)
def read_users(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    users = session.scalars(
        select(User).offset(skip).limit(limit)
    ).all()

    return {
        'users': users,
        'total': len(users)
    }
