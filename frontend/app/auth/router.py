from fastapi import APIRouter, Depends, Request
from aiohttp import ClientSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse



templates = Jinja2Templates(directory = './app/auth/templates')



router = APIRouter(
                prefix = '/auth',
                tags = ['Аунтификация']
                )




@router.get(path = '/login', summary = 'Вход в аккаунт')
async def login(request : Request) -> HTMLResponse:
    return templates.TemplateResponse(
        'login.html', {'request': request}
    )
    
    
@router.get(path = '/registrate', summary = 'Вход в аккаунт')
async def registrate(request : Request) -> HTMLResponse:
    return templates.TemplateResponse(
        'registrate.html', {'request': request}
    )

    
    
@router.get(path = '/seller-registrate', summary = 'Стать продавцом')
async def seller_registate(request : Request) -> HTMLResponse:
    return templates.TemplateResponse(
        'seller_registrate.html', {'request': request}
    )
