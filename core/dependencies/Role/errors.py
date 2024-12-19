from core.exception.BaseHTTPException import BaseHTTPExceptionModel
from core.dependencies.JWTToken import JWTException
from enum import StrEnum, auto
from fastapi import status
from pydantic import ConfigDict





class RoleErrorType(StrEnum):
    INCORRECT_ROLE = auto()


    
    
class RoleExceptionModel(BaseHTTPExceptionModel):
    
    type : RoleErrorType
    
    model_config = ConfigDict(title = 'Ошибка выдачи прав')
    
    
    
class RoleException(JWTException):
    pass


NoRightError = RoleException(status_code = status.HTTP_403_FORBIDDEN, 
                                    ditail = RoleExceptionModel(
                                        type = RoleErrorType.INCORRECT_ROLE,
                                        message = 'you havent right'
                                    )
                            )