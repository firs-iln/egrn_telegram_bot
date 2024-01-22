from enum import Enum as pyEnum


class UserRolesEnum(pyEnum):
    """User roles."""

    USER = 'user'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'


class RequestStatusEnum(pyEnum):
    """Request statuses."""

    CREATED = 'created'
    WAITINGFOREXTRACT = 'waiting_for_extract'
    EXTRACTDONE = 'extract_done'
    R1R7DONE = 'r1r7_done'
    WAITINGFORPROCESSING = 'waiting_for_processing'
    REESTRDONE = 'reestr_done'
    CANCELED = 'canceled'
