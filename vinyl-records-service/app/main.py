from fastapi import FastAPI
from core.exception import BaseHTTPException, http_Exception_handler
from .action import action_router
from .search import search_router



app = FastAPI(  
        root_path = '/api',
        exception_handlers = {
            BaseHTTPException : http_Exception_handler
    }
)


app.include_router(action_router)
app.include_router(search_router)




