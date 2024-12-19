from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class BucketErrorType(StrEnum):
    CAN_NOT_INSERT = auto()
    INCCORECT_ID = auto()




class BucketExceptionModel(BaseHTTPExceptionModel):
    
    type : BucketErrorType
 
    model_config = ConfigDict(title = 'Ошибка регистации')




class BucketException(BaseHTTPException):
    pass



BucketInsertError = BucketException(status_code = status.HTTP_400_BAD_REQUEST,
                                    ditail = BucketExceptionModel(
                                        type = BucketErrorType.CAN_NOT_INSERT,
                                        message = 'this vinyl record already in bucket'
                                    )
                                )

VinylRecordNotPresentError = BucketException(status_code = status.HTTP_400_BAD_REQUEST,
                                    ditail = BucketExceptionModel(
                                        type = BucketErrorType.INCCORECT_ID,
                                        message = 'this vinyl record not present in bucket'
                                    )
                                )

