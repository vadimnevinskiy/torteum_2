from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
