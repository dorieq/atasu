from enum import Enum

class UserRolesEnum(Enum):  
    USER = 'USER'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)