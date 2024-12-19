from enum import StrEnum, auto



class OrderStatus(StrEnum):

    created = auto()
    assembled = auto()
    in_delivery = auto()
    delivered = auto()
    canceled = auto()
    