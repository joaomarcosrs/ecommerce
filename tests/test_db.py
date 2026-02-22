from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.orm import Session

from ecommerce.core.database import get_session
from ecommerce.users.models import User


def test_get_session_function():
    session_gen = get_session()
    session = next(session_gen)
    assert session is not None
    # finaliza o generator
    try:
        next(session_gen)
    except StopIteration:
        pass


def test_create_user(session: Session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            name='John Doe',
            email='john.doe@example.com',
            password='123456',
            phone_number=None
        )
        session.add(new_user)
        session.commit()

    user_db = session.scalar(
        select(User).where(
            User.email == 'john.doe@example.com'
        )
    )

    assert asdict(user_db) == {
        'id': 1,
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': '123456',
        'phone_number': None,
        'public_id': user_db.public_id,
        'created_at': time,
        'updated_at': time
    }
