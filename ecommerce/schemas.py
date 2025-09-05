from datetime import datetime

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    public_id: str
    name: str
    email: EmailStr
    phone_number: str | None = None
    created_at: datetime
    updated_at: datetime
