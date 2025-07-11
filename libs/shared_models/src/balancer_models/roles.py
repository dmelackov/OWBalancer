from enum import Enum


class Roles(Enum):
    GUEST = "Guest"
    CUSTOMER = "Customer"
    MODERATOR = "Moderator"
    ADMINISTRATOR = "Administrator"
