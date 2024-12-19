from pydantic import Field, ConfigDict, field_serializer, PositiveInt, computed_field, PrivateAttr
from .BaseModel import BaseModel
from enum import StrEnum, auto
from datetime import datetime
from .vinyl_record import VinylRecordID


class SuccessUserActionStatusType(StrEnum):
    SUCCESS_INSERT = auto()
    SUCCESS_UPDATE = auto()
    SUCCESS_DELETE = auto()
    


class UserActionOut(BaseModel):
    
    status : SuccessUserActionStatusType = Field(description = 'Статус изменения')
    
    model_config = ConfigDict(title = 'Успешное завершение изменения')
    
 