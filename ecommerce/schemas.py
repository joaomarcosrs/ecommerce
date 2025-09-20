from datetime import datetime

from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str | None = None


class UserRead(BaseModel):
    public_id: str
    name: str
    email: EmailStr
    phone_number: str | None = None
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    current_password: str | None = None
    password: str | None = None


class UserList(BaseModel):
    users: list[UserRead]
    total: int


class Token(BaseModel):
    access_token: str
    token_type: str
