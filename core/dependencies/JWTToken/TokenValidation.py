from .JWTToken import JWTToken
from fastapi import Request, Security
from fastapi.security.api_key import APIKeyHeader
from jwt import InvalidTokenError, ExpiredSignatureError
from .JWTTokenType import JWTTokenType
from .errors import *
from .dao import JWTTokenDAO
from typing import Any
from .schemas import IssuedJWTTokenPayloadOut




class TokenValidation:



    @staticmethod
    def __try_to_get_clear_token(authorization_header: str) -> str:
        if authorization_header is None:
            raise IsNotSpecifiedError

        if 'Bearer ' not in authorization_header:
            raise IncorrectAuthHeaderFromError

        return authorization_header.removeprefix('Bearer ')



    @staticmethod
    def check_token_payload(token : str, type_ : JWTTokenType) -> dict[str, Any]:
        try:
            payload = JWTToken.verify_token(token)
        except ExpiredSignatureError:
            raise ExpiredTokenError
        
        except InvalidTokenError:
            raise ClientInvalidTokenError
        
        if payload['type'] != type_:
            raise IncorrectTokenTypeError

        return payload
    
    

    @classmethod
    async def check_access_token(
        cls,
        request: Request,
        authorization_header: str = Security(APIKeyHeader(name = 'Authorization', auto_error = False))
    ) -> str:
        
        clear_token = cls.__try_to_get_clear_token(authorization_header = authorization_header)

        payload = cls.check_token_payload(clear_token, JWTTokenType.ACCESS)
        
        await JWTTokenDAO.check_token_is_remove(payload['jti'])
        
        request.state.user = IssuedJWTTokenPayloadOut.model_validate(payload)
        request.state.error = None
        
        return authorization_header
    
    
    
    @classmethod
    def check_refresh_token(
        cls,
        refresh_token : str
    ) -> IssuedJWTTokenPayloadOut:
        
        payload = cls.check_token_payload(refresh_token, JWTTokenType.REFRESH)
        return IssuedJWTTokenPayloadOut.model_validate(payload)
        
    

    @classmethod
    async def weak_check_access_token(
        cls,
        request: Request,
        authorization_header: str = Security(APIKeyHeader(name = 'Authorization', auto_error = False))
    ) -> str | None:
        try:
            return await cls.check_access_token(request = request, authorization_header = authorization_header)
        except JWTException as error:
            request.state.error = error
            request.state.user = None
            
            
        


    @staticmethod
    async def check_access_token_after_weak_check(
        request: Request
    ) -> None:
        if request.state.error is not None:
            raise request.state.error
        