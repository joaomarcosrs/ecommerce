from datetime import datetime
from http import HTTPStatus

import ulid
from fastapi import FastAPI

from ecommerce.schemas import User, UserRead

app = FastAPI()


@app.post("/users", status_code=HTTPStatus.CREATED, response_model=UserRead)
def create_user(user: User):
    user_created = UserRead(
        public_id=str(ulid.new()),
        name=user.name,
        email=user.email,
        phone_number=None,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    return user_created
