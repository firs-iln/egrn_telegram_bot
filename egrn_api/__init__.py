from .types import SearchResponse
from .EgrnApiRepo import EGRNAPI
from config import config

__all__ = ["SearchResponse", "EGRNAPI"]

api = EGRNAPI(config.EGRN_API_TOKEN.get_secret_value())
