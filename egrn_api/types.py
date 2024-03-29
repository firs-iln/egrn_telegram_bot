from pydantic import BaseModel, Field
from typing import Optional


class PrevNum(BaseModel):
    type: str
    value: str


class Right(BaseModel):
    right: str
    restriction: Optional[str] = ''


class RnbRight(BaseModel):
    right_origin: str
    right_reg_number: str
    right_reg_date: Optional[str] = ''
    right_description: str


class RnbBound(BaseModel):
    bound_origin: str
    bound_description: str
    bound_reg_number: str


class Rnb(BaseModel):
    rights: list[RnbRight] = []
    bounds: list[RnbBound] = []


class SearchResponseItem(BaseModel):
    cad_num: str
    obj_type: str
    address: str
    status: str
    reg_date: str
    area: str
    unit: str
    cad_cost: Optional[str] = ''
    cost_insertion_date: Optional[str] = ''
    cost_definition_date: Optional[str] = ''
    oks_type: Optional[str] = ''
    oks_type_more: Optional[str] = ''
    oks_purpose: Optional[str] = ''
    refresh_date: str
    floor: Optional[str] = ''
    ownersheep_type: str
    update_date: str
    rights: list[Right] = []
    rnb: Optional[Rnb] = None
    notes: list
    prev_nums: list[PrevNum] = []


class SearchResponse(BaseModel):
    query: str
    found: int
    results: list[SearchResponseItem] = Field(alias="list")


class CreateRequestResponse(BaseModel):
    order_id: str


class CheckRequestResponse(BaseModel):
    order_id: str
    status: str
    creation_dt: str
    fgis_key_name: Optional[str] = ''
    rr_status: Optional[str] = ''
    rr_number: Optional[str] = ''
    rr_sent_dt: Optional[str] = ''
    complete: int


class DownloadOrderResponse(BaseModel):
    file_bytes: bytes
    filename: str
