from fastapi import FastAPI
from core.exception import BaseHTTPException, http_Exception_handler
from .auth import auth_router
from fastapi.staticfiles import StaticFiles




app = FastAPI(  
        root_path = '/api/auth',
        exception_handlers = {
        BaseHTTPException : http_Exception_handler
    }
)

app.include_router(auth_router)