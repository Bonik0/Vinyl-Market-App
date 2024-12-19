from fastapi import FastAPI
from core.exception import BaseHTTPException, http_Exception_handler
from fastapi.staticfiles import StaticFiles
from .vinyl_records import vinyl_record_router
from .auth import auth_router
from .user import user_router
from .seller import seller_router



app = FastAPI(
        exception_handlers = {
            BaseHTTPException : http_Exception_handler
    }
)


app.mount('/static/seller', StaticFiles(directory = './app/seller-static'), name = 'seller-static')
app.mount('/static/me', StaticFiles(directory = './app/user-static'), name = 'user-static')
app.mount('/static/auth', StaticFiles(directory = './app/auth-static') , name = 'auth-static')
app.mount('/static/vinyl-records', StaticFiles(directory = './app/vinyl-records-static') , name = 'vinyl-records-static')
app.mount('/static', StaticFiles(directory = './app/main-static'), name = 'static')


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(seller_router)
app.include_router(vinyl_record_router)


