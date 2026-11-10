from pydantic import BaseModel


class ResponseMessage(BaseModel):
    status_code: int
    message: str

    model_config = {"from_attributes": True}
