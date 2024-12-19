from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class SellerOrderErrorType(StrEnum):
    CANT_CANCEL = auto()



class SellerOrderExceptionModel(BaseHTTPExceptionModel):
    
    type : SellerOrderErrorType
 
    model_config = ConfigDict(title = 'Ошибка регистации')




class SellerOrderException(BaseHTTPException):
    pass



OrderChengeStatusError = SellerOrderException(status_code = status.HTTP_400_BAD_REQUEST,
                                    ditail = SellerOrderExceptionModel(
                                        type = SellerOrderErrorType.CANT_CANCEL,
                                        message = 'is not you order or order already delivered(canceled)'
                                    )
                                )