from pydantic import BaseModel, ConfigDict
from typing import Optional


class RequestBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    id: Optional[int] = None
    cadnum: Optional[str] = None
    fio_is_provided: bool = False
    price: Optional[int] = None


class RequestCreate(RequestBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    cadnum: str
    fio_is_provided: bool


class RequestResponse(RequestBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    id: int
    cadnum: str
    fio_is_provided: bool
    price: Optional[int] = None
