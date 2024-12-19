from enum import StrEnum, auto



class UserRole(StrEnum):
    user = auto()
    seller = auto()
    admin = auto()
    
    def is_admin(self : 'UserRole') -> bool:
        return self == UserRole.admin