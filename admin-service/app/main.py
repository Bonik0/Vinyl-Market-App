from fastapi import FastAPI, Depends
from core.exception import BaseHTTPException, http_Exception_handler
from core.dependencies.Role import RoleException, RoleValidation
from core.models.postgres import UserRole



app = FastAPI(  
        root_path = '/admin',
        dependencies = [Depends(RoleValidation.check_role_right(UserRole.admin))],
        responses = RoleException.get_responses_schemas(),
        exception_handlers = {
        BaseHTTPException : http_Exception_handler
    }
)
