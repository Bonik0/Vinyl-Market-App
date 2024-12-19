from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class SellerVinylRecordErrorType(StrEnum):
    INCORRECT_ID = auto()
    TITLE_ALREADY_EXIST = auto()
    NOT_CLOSE_ORDERS = auto()




class SellerVinylRecordExceptionModel(BaseHTTPExceptionModel):
    
    type : SellerVinylRecordErrorType
 
    model_config = ConfigDict(title = 'Ошибка регистации')




class SellerVinylRecordException(BaseHTTPException):
    pass



IncorrectIDError = SellerVinylRecordException(status_code = status.HTTP_404_NOT_FOUND,
                                        ditail = SellerVinylRecordExceptionModel(
                                            type = SellerVinylRecordErrorType.INCORRECT_ID,
                                            message = 'you are have not this vinyl record'
                                        )
                                    )

UniqueVinylRecordError = SellerVinylRecordException(status_code = status.HTTP_404_NOT_FOUND,
                                        ditail = SellerVinylRecordExceptionModel(
                                            type = SellerVinylRecordErrorType.TITLE_ALREADY_EXIST,
                                            message = 'this vinyl record title already exist'
                                        )
                                    )

DeleteVinylRecordError = SellerVinylRecordException(status_code = status.HTTP_404_NOT_FOUND,
                                        ditail = SellerVinylRecordExceptionModel(
                                            type = SellerVinylRecordErrorType.NOT_CLOSE_ORDERS,
                                            message = 'you have open orders and cant delete this vinyl'
                                        )
                                    )

