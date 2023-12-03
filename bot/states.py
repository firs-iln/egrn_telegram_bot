from enum import Enum


class MainDialogStates(Enum):
    EGRN_CHOSE = 'egrn_chose'
    GET_DOC = 'get_doc'
    CHOOSE_OPTION = 'choose_option'
    FLOORS_PICS = 'floor_pics'
    ONLINE_CONFIRM = 'online_confirm'
    CHOOSE_OPTION_REGISTRY = 'choose_option_registry'
    FIO_TEST_ASKED_REGISTRY = 'fio_test_asked_registry'
    ASKED_TABLE = 'asked_table'
    ASKED_CAD = 'asked_cad'
    ASKED_NAMES = 'asked_names'
    ASKED_REG = 'asked_reg'
    ASKED_EXTRACT = 'asked_extract'
    ASKED_PARTS = 'asked_parts'
    WAIT = 'wait'
