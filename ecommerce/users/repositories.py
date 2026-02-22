from sqlalchemy import select
from sqlalchemy.orm import Session

from ecommerce.users.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_public_id(self, public_id: str) -> User | None:
        return self.session.scalar(
            select(User).where(User.public_id == public_id)
        )

    def get_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))

    def get_by_phone_number(self, phone_number: str) -> User | None:
        return self.session.scalar(
            select(User).where(User.phone_number == phone_number)
        )

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
