from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class VinylRecordErrorType(StrEnum):
    INCORRECT_ID = auto()




class VinylRecordExceptionModel(BaseHTTPExceptionModel):
    
    type : VinylRecordErrorType
 
    model_config = ConfigDict(title = 'Ошибка регистации')




class VinylRecordException(BaseHTTPException):
    pass



IncorrectIDError = VinylRecordException(status_code = status.HTTP_404_NOT_FOUND,
                                        ditail = VinylRecordExceptionModel(
                                            type = VinylRecordErrorType.INCORRECT_ID,
                                            message = 'have not this vinyl record id'
                                        )
                                    )