from datetime import datetime

from pydantic import BaseModel, EmailStr


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


class UserList(BaseModel):
    users: list[UserRead]
    total: int
