from core.dependencies.JWTToken import TokenValidation
from core.models.postgres import UserRole
from fastapi import Request, Security
from fastapi.security.api_key import APIKeyHeader
from .errors import NoRightError


class RoleValidation:
    
    @staticmethod
    def check_role_right(role : UserRole):
        
        async def wrapper(
                    request: Request,
                    authorization_header: str = Security(APIKeyHeader(name = 'Authorization', auto_error = False))
                ) -> None:
    
            await TokenValidation.check_access_token(request, authorization_header)
            
            user_role = UserRole(request.state.user.role)
           
            if role == user_role:
                return
            
            raise NoRightError
            
            
        return wrapper
        