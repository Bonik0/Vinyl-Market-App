from fastapi import FastAPI, Depends
from core.exception import BaseHTTPException, http_Exception_handler
from core.dependencies.Role import RoleException, RoleValidation
from core.models.postgres import UserRole
from .vinyl_records import vinyl_record_router
from .order import order_router


app = FastAPI(  
        root_path = '/api/seller',
        dependencies = [Depends(RoleValidation.check_role_right(UserRole.seller))],
        responses = RoleException.get_responses_schemas(),
        exception_handlers = {
        BaseHTTPException : http_Exception_handler
    }
)


app.include_router(vinyl_record_router)
app.include_router(order_router)
