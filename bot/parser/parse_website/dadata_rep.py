import os

from dadata import Dadata
from pydantic import BaseModel
from typing import Any, Optional


class DadataAddress(BaseModel):
    source: Optional[str] = None
    result: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    country_iso_code: Optional[str] = None
    federal_district: Optional[str] = None
    region_fias_id: Optional[str] = None
    region_kladr_id: Optional[str] = None
    region_iso_code: Optional[str] = None
    region_with_type: Optional[str] = None
    region_type: Optional[str] = None
    region_type_full: Optional[str] = None
    region: Optional[str] = None
    area_fias_id: Optional[str] = None
    area_kladr_id: Optional[str] = None
    area_with_type: Optional[str] = None
    area_type: Optional[str] = None
    area_type_full: Optional[str] = None
    area: Optional[str] = None
    city_fias_id: Optional[str] = None
    city_kladr_id: Optional[str] = None
    city_with_type: Optional[str] = None
    city_type: Optional[str] = None
    city_type_full: Optional[str] = None
    city: Optional[str] = None
    city_area: Optional[str] = None
    city_district_fias_id: Optional[str] = None
    city_district_kladr_id: Optional[str] = None
    city_district_with_type: Optional[str] = None
    city_district_type: Optional[str] = None
    city_district_type_full: Optional[str] = None
    city_district: Optional[str] = None
    settlement_fias_id: Optional[str] = None
    settlement_kladr_id: Optional[str] = None
    settlement_with_type: Optional[str] = None
    settlement_type: Optional[str] = None
    settlement_type_full: Optional[str] = None
    settlement: Optional[str] = None
    street_fias_id: Optional[str] = None
    street_kladr_id: Optional[str] = None
    street_with_type: Optional[str] = None
    street_type: Optional[str] = None
    street_type_full: Optional[str] = None
    street: Optional[str] = None
    stead_fias_id: Optional[str] = None
    stead_kladr_id: Optional[str] = None
    stead_cadnum: Optional[str] = None
    stead_type: Optional[str] = None
    stead_type_full: Optional[str] = None
    stead: Optional[str] = None
    house_fias_id: Optional[str] = None
    house_kladr_id: Optional[str] = None
    house_cadnum: Optional[str] = None
    house_type: Optional[str] = None
    house_type_full: Optional[str] = None
    house: Optional[str] = None
    block_type: Optional[str] = None
    block_type_full: Optional[str] = None
    block: Optional[str] = None
    entrance: Optional[str] = None
    floor: Optional[str] = None
    flat_fias_id: Optional[str] = None
    flat_cadnum: Optional[str] = None
    flat_type: Optional[str] = None
    flat_type_full: Optional[str] = None
    flat: Optional[str] = None
    flat_area: Optional[str] = None
    square_meter_price: Optional[str] = None
    flat_price: Optional[str] = None
    postal_box: Optional[str] = None
    fias_id: Optional[str] = None
    fias_code: Optional[str] = None
    fias_level: Optional[int] = None
    fias_actuality_state: Optional[str] = None
    kladr_id: Optional[str] = None
    capital_marker: Optional[str] = None
    okato: Optional[str] = None
    oktmo: Optional[str] = None
    tax_office: Optional[str] = None
    tax_office_legal: Optional[str] = None
    timezone: Optional[str] = None
    geo_lat: Optional[str] = None
    geo_lon: Optional[str] = None
    beltway_hit: Optional[str] = None
    beltway_distance: Optional[str] = None
    qc_geo: Optional[int] = None
    qc_complete: Optional[int] = None
    qc_house: Optional[int] = None
    qc: Optional[int] = None
    unparsed_parts: Optional[str] = None
    metro: Optional[list[dict[str, Any]]] = None


class DadataRepository:
    def __init__(self, token, secret):
        self.dadata = Dadata(token, secret)

    def get_fias_id(self, address: str) -> str:
        response = self.dadata.clean("address", address)
        return DadataAddress(**response).fias_id

    def get_data(self, address: str) -> DadataAddress:
        response = self.dadata.clean("address", address)
        return DadataAddress(**response)


API_KEY = os.environ.get('DADATA_API_KEY')
SECRET_KEY = os.environ.get('DADATA_SECRET_KEY')
# print(API_KEY, SECRET_KEY)
dadata = DadataRepository(API_KEY, SECRET_KEY)
# dadata.get_fias_id("fdghjkl")