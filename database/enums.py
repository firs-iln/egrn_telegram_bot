from enum import Enum as pyEnum


class UserRolesEnum(pyEnum):
    """User roles."""

    USER = 'user'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'


class ClientTypeEnum(pyEnum):
    """Client type enum."""

    INDIVIDUAL = 'individual'
    LEGAL = 'legal'
