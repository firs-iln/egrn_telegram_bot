from pydantic import BaseModel


class PrevNum(BaseModel):
    type: str
    value: str


class Right(BaseModel):
    right: str
    restriction: str


class RnbRight(BaseModel):
    right_origin: str
    right_reg_number: str
    right_reg_date: str
    right_description: str


class Rnb(BaseModel):
    rights: list[RnbRight]
    bounds: list


class SearchResponseItem(BaseModel):
    cad_num: str
    obj_type: str
    address: str
    status: str
    reg_date: str
    area: str
    unit: str
    cad_cost: str
    cost_insertion_date: str
    cost_definition_date: str
    oks_type: str
    oks_type_more: str
    oks_purpose: str
    refresh_date: str
    floor: str
    ownersheep_type: str
    update_date: str
    rights: list[Right]
    rnb: Rnb
    notes: list
    prev_nums: list[PrevNum]


class SearchResponse(BaseModel):
    query: str
    found: int
    list: list[SearchResponseItem]
