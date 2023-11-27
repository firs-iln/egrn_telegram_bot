from .PageParser import PageParser
import selenium.common.exceptions as e
from .exceptions import NotEnoughMoneyException


def parse_building(cad_id: str):
    page_parser = PageParser()
    building = page_parser.parse(cad_id)
    return building


def parse_land(cad_id: str):
    page_parser = PageParser()
    building = page_parser.parse(cad_id)
    return building


def parse_room(cad_id):
    page_parser = PageParser()
    cad_id = cad_id.split(', ')
    # print("cad_id =", cad_id)
    rooms = {}
    for cad in cad_id:
        try:
            rooms[cad] = page_parser.parse(cad)
        except (e.NoSuchElementException, e.TimeoutException):
            rooms[cad] = None
        except NotEnoughMoneyException:
            try:
                rooms[cad] = page_parser.parse(cad)
            except (e.NoSuchElementException, e.TimeoutException):
                rooms[cad] = None
            except NotEnoughMoneyException:
                rooms[cad] = None
        except e.WebDriverException:
            return parse_room(', '.join(cad_id))
    return rooms


def parse_site(cad_id: str, cad_ids: list[str]):
    building = parse_building(cad_id)
    rooms = parse_rooms(cad_ids)
    return building, rooms
