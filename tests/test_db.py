from sqlalchemy import select
from sqlalchemy.orm import Session

from ecommerce.models import User


def test_create_user(session: Session):
    user = User(
        name='John Doe',
        email='john.doe@example.com',
        password='123456',
        phone_number=None
    )
    session.add(user)
    session.commit()

    user_db = session.scalar(
        select(User).where(
            User.email == 'john.doe@example.com'
        )
    )

    assert user_db is not None
    assert user_db.name == 'John Doe'
    assert user_db.email == 'john.doe@example.com'
    assert user_db.password == '123456'
    assert user_db.phone_number is None
    assert user_db.public_id is not None
    assert user_db.created_at is not None
    assert user_db.updated_at is not None
