from enum import Enum


class MainDialogStates(Enum):
    EGRN_CHOSE = 'egrn_chose'
    GET_DOC = 'get_doc'
    CHOOSE_OPTION = 'choose_option'
    FLOORS_PICS = 'floor_pics'
    CHOOSE_OPTION_REGISTRY = 'choose_option_registry'
    FIO_TEST_ASKED_REGISTRY = 'fio_test_asked_registry'
    ASKED_TABLE = 'asked_table'
    ASKED_CAD = 'asked_cad'
    ASKED_NAMES = 'asked_names'
    ASKED_REG = 'asked_reg'
    ASKED_EXTRACT = 'asked_extract'
    ASKED_PARTS = 'asked_parts'
    WAIT = 'wait'


class ApiDialogStates:
    ASKED_EXTRACT = 'asked_extract'
    CONFIRM_R1R7 = 'confirm_r1r7'
    EDIT_R1R7 = 'edit_r1r7'
    CONFIRMED_R1R7 = 'confirmed_r1r7'

    CONFIRM_REGISTRY = 'confirm_registry'
    EDIT_REGISTRY = 'edit_registry'
    CONFIRMED_REGISTRY = 'confirmed_registry'

    ASKED_CAD_COLUMN = 'asked_cad_column'
    ASKED_NAMES_COLUMN = 'asked_names_column'
    ASKED_REG_COLUMN = 'asked_reg_column'
    ASKED_EXTRACT_COLUMN = 'asked_extract_column'
    ASKED_PARTS_COLUMN = 'asked_parts_column'
