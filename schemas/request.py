from pydantic import BaseModel, ConfigDict
from typing import Optional


class RequestBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    id: Optional[int] = None
    cadnum: Optional[str] = None
    order_id: Optional[int] = None
    fio_is_provided: bool = False


class RequestCreate(RequestBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    cadnum: str
    order_id: int
    fio_is_provided: bool


class RequestResponse(RequestBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    id: int
    cadnum: str
    order_id: int
    r1r7_filename: Optional[str]
    registry_filename: Optional[str]
    fio_is_provided: bool
