from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    first_name: str
    last_name: str | None
    email: str


class UserCreate(User):
    password_hash: str


class UserResponse(User):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
