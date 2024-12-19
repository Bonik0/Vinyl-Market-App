from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class UserOrderErrorType(StrEnum):
    ZERO_QUANTITY = auto()
    CANT_CANCEL = auto()



class UserOrderExceptionModel(BaseHTTPExceptionModel):
    
    type : UserOrderErrorType
 
    model_config = ConfigDict(title = 'Ошибка регистации')




class UserOrderException(BaseHTTPException):
    pass



VinylZeroQuantityError = UserOrderException(status_code = status.HTTP_400_BAD_REQUEST,
                                    ditail = UserOrderExceptionModel(
                                        type = UserOrderErrorType.ZERO_QUANTITY,
                                        message = 'this vinyl record have zero quantity'
                                    )
                                )

OrderCancelError = UserOrderException(status_code = status.HTTP_400_BAD_REQUEST,
                                    ditail = UserOrderExceptionModel(
                                        type = UserOrderErrorType.CANT_CANCEL,
                                        message = 'is not you order or order already delivered(canceled)'
                                    )
                                )