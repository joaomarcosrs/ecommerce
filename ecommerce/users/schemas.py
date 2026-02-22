from datetime import datetime

from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    current_password: str | None = None
    password: str | None = None


class UserRead(UserBase):
    public_id: str
    created_at: datetime
    updated_at: datetime
