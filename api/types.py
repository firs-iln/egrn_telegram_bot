from pydantic import BaseModel


class OrderCallbackInput(BaseModel):
    price: int
