from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Alignment

from selenium.common.exceptions import WebDriverException, TimeoutException

from .parse_web import parse_land, parse_building, parse_room


class CadObject:
    cad_id: str
    card: str

    def set_card(self, card: dict):
        res = ''
        for div, subdict in card.items():
            res += div
            for key, string in subdict.items():
                res += key.strip()
                res += string.strip()
        self.card = res.strip()

    def __eq__(self, other: str):
        if not isinstance(other, str):
            return False
        return self.cad_id == other


class Room(CadObject):
    pass


class Building(CadObject):
    address: str
    rooms: list[Room]

    def __init__(self):
        super().__init__()
        self.rooms = []

    def find_room(self, cad_id: str):
        return self.rooms[self.rooms.index(cad_id)]

    def set_room_card(self, room_id: str, card: dict):
        try:
            self.find_room(room_id).set_card(card)
        except ValueError:
            pass


class Land(CadObject):
    building: Building

    def set_id(self, cad_id):
        if cad_id in ('данные отсутствуют', self.building.cad_id):
            return
        self.cad_id = cad_id

    @property
    def exists(self):
        return self.cad_id != 'данные отсутствуют'


class Parser:
    def __init__(self, src):
        self.land = Land()
        self.land.building = Building()
        self.src = src

    def get_objects_from_seventh(self) -> None:
        wb: Workbook = load_workbook(self.src)

        ws_first: Worksheet = wb.get_sheet_by_name("Раздел 1")
        ws_seventh: Worksheet = wb.get_sheet_by_name("Раздел 7")

        self.land.building.cad_id = ws_first["B2"].value
        self.land.building.address = ws_first["B6"].value

        self.land.cad_id = ws_first["B15"].value

        for row in [x for x in ws_seventh.rows][1:]:
            room = Room()
            room.cad_id = row[1].value
            self.land.building.rooms.append(room)

    def parse_objects(self):
        if self.land.exists:
            land = None
            try:
                land = parse_land(self.land.cad_id)
            except TimeoutException:
                print('one more time...')
                land = parse_land(self.land.cad_id)
            if land:
                self.land.set_card(land)

        building = None
        try:
            building = parse_building(self.land.building.cad_id)
        except TimeoutException:
            print('one more time...')
            building = parse_building(self.land.building.cad_id)
        if building:
            self.land.building.set_card(building)

        for i, room in enumerate(self.land.building.rooms):
            not_got = True
            while not_got:
                try:
                    roomreses: dict = parse_room(room.cad_id)
                    if all(roomreses.values()):
                        not_got = False
                except WebDriverException:
                    pass
            print(room.cad_id, roomreses)
            for room_id, room_card in roomreses.items():
                print(room_id, room_card)
                self.land.building.set_room_card(room_id, room_card)

    def write_objects(self):

        # print(1111, *map(lambda x: x.cad_id, self.land.building.rooms))

        wb: Workbook = load_workbook(self.src)

        ws_first: Worksheet = wb.get_sheet_by_name("Раздел 1")
        ws_seventh: Worksheet = wb.get_sheet_by_name("Раздел 7")

        ws_first["C2"] = self.land.building.card

        if self.land.exists:
            ws_first["C15"] = self.land.card

        # print(*list(map(lambda x: x.cad_id, self.land.building.rooms)))

        for i, row in enumerate([x for x in ws_seventh.rows][1:]):
            cad_id = row[1].value
            # print(cad_id)
            room = self.land.building.find_room(cad_id)
            ws_seventh.cell(row=i + 2, column=8).value = self.land.building.cad_id
            card_cell = ws_seventh.cell(row=i + 2, column=9)
            card_cell.value = room.card
            card_cell.alignment = Alignment(wrapText=True)

        wb.save(self.src)

    def process_objects(self):
        self.get_objects_from_seventh()
        self.parse_objects()
        self.write_objects()


if __name__ == '__main__':
    src = input()
    parser_obj = Parser(src)
    parser_obj.process_objects()
