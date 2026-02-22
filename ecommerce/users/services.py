from pydantic import EmailStr

from ecommerce.core.security import get_password_hash, verify_password
from ecommerce.users.models import User
from ecommerce.users.repositories import UserRepository
from ecommerce.users.schemas import UserUpdate


class EmailAlreadyExistsError(Exception): ...


class PhoneNumberAlreadyExistsError(Exception): ...


class UserNotFoundError(Exception): ...


class InvalidCredentialsError(Exception): ...


class PasswordChangeValidationError(Exception): ...


class InvalidCurrentPasswordError(Exception): ...


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(
        self,
        *,
        email: EmailStr,
        password: str,
        name: str,
        phone_number: str | None = None,
    ) -> User:
        if self.repo.get_by_email(str(email)):
            raise EmailAlreadyExistsError()

        if phone_number and self.repo.get_by_phone_number(phone_number):
            raise PhoneNumberAlreadyExistsError()

        user = User(
            email=str(email),
            name=name,
            phone_number=phone_number,
            password=get_password_hash(password),
        )
        return self.repo.create(user)

    def get_user_by_public_id(self, public_id: str) -> User:
        user = self.repo.get_by_public_id(public_id)
        if not user:
            raise UserNotFoundError()
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.repo.get_by_email(email)
        if not user:
            raise UserNotFoundError()
        return user

    def update_user(self, *, public_id: str, payload: UserUpdate) -> User:
        user = self.get_user_by_public_id(public_id)

        if payload.email and payload.email != user.email:
            existing_user_by_email = self.repo.get_by_email(str(payload.email))
            if existing_user_by_email:
                raise EmailAlreadyExistsError()

        if payload.phone_number and payload.phone_number != user.phone_number:
            existing_user_by_phone = self.repo.get_by_phone_number(
                payload.phone_number
            )
            if existing_user_by_phone:
                raise PhoneNumberAlreadyExistsError()

        has_password_fields = (
            payload.password is not None
            or payload.current_password is not None
        )

        if has_password_fields:
            if not payload.current_password or not payload.password:
                raise PasswordChangeValidationError()

            if not verify_password(payload.current_password, user.password):
                raise InvalidCurrentPasswordError()

            payload.password = get_password_hash(payload.password)
        else:
            payload.current_password = None
            payload.password = None

        update_data = payload.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        return self.repo.update(user)

    def delete_user(self, *, public_id: str) -> None:
        user = self.get_user_by_public_id(public_id)
        self.repo.delete(user)

    def authenticate(self, *, email: str, password: str) -> User:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            raise InvalidCredentialsError()
        return user
