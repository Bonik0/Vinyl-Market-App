from fastapi import FastAPI, Depends
from core.exception import BaseHTTPException, http_Exception_handler
from .account import account_router
from .bucket import bucket_router
from .order import order_router
from core.dependencies.JWTToken import JWTException, TokenValidation


app = FastAPI(  
        root_path = '/api/me',
        exception_handlers = {
        BaseHTTPException : http_Exception_handler
        },
        dependencies = [Depends(TokenValidation.check_access_token)],
        responses = JWTException.get_responses_schemas()
)



app.include_router(bucket_router)
app.include_router(account_router)
app.include_router(order_router)