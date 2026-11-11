from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    # для того чтобы кастомизировать ошибки, сделал допуск None для обязательных полей,
    # но нужно принять архитектурное решение и убрать такой допуск
    first_name: str | None
    last_name: str | None
    email: EmailStr | None


class UserCreate(User):
    password_hash: str | None


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password_hash: str | None = None


class UserResponse(User):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
