from .Base import Base, async_session_maker
from .UserRole import UserRole
from .OrderStatus import OrderStatus

MAX_SMALL_INT_VALUE : int = 32_767
MAX_VARCHAR_VALUE : int = 255
MIN_VARCHAR_VALUE : int = 1
MAX_BIG_INT_VALUE : int = 9_000_000_000_000_000_000
MAX_INT_OR_FLOAT_VALUE : int = 2_147_483_647



__all__ = ['Base', 'async_session_maker', 'UserRole', 'OrderStatus']