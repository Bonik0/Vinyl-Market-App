from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class AuthErrorType(StrEnum):
    EMAIL_OCCUPIED = auto()
    USERNAME_OCCUPIED = auto()
    INVALID_USERNAME_OR_EMAIL = auto()
    INVALID_PASSWORD = auto()
    YOU_ARE_SELLER = auto()




class AuthExceptionModel(BaseHTTPExceptionModel):
    
    type : AuthErrorType
 
    model_config = ConfigDict(title = 'Ошибка регистации')




class AuthException(BaseHTTPException):
    pass




EmailOccupiedError = AuthException(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExceptionModel(
                                                                    type = AuthErrorType.EMAIL_OCCUPIED,
                                                                    message = 'This email is already occupied'
                                                                )
                                         )

UsernameOccupiedError = AuthException(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExceptionModel(
                                                                    type = AuthErrorType.USERNAME_OCCUPIED,
                                                                    message = 'This username is already occupied'
                                                                )
                                         )


InvalidUsernameOrEmailError = AuthException(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExceptionModel(
                                                                    type = AuthErrorType.INVALID_USERNAME_OR_EMAIL,
                                                                    message = 'This username or email not registrate'
                                                                )
                                         )

InvalidPasswordError = AuthException(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExceptionModel(
                                                                    type = AuthErrorType.INVALID_PASSWORD,
                                                                    message = 'This password is inccorect'
                                                                )
                                         )

RepeatRegistratesellerError = AuthException(status_code = status.HTTP_400_BAD_REQUEST,
                                         ditail = AuthExceptionModel(
                                                                    type = AuthErrorType.YOU_ARE_SELLER,
                                                                    message = 'you are seller'
                                                                )
                                         )



