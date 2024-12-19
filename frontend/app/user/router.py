from fastapi import APIRouter, Depends, Request, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from core.schemas import VinylRecordOut, VinylRecordID
from typing import Annotated
from aiohttp import ClientSession
from math import ceil



templates = Jinja2Templates(directory = './app/user/templates')



router = APIRouter(
                    prefix = '/me',
                    tags = ['Аккаунт']
                )




@router.get(path = '/account-info', summary = 'Информация о пользователе')
async def user_account_info(request : Request) -> HTMLResponse:
    
    headers = {}
    if request.headers.get('Authorization') is not None:
        headers['Authorization'] = request.headers.get('Authorization')
        
    async with ClientSession() as session:
        response = await session.get('http://user-service:8000/api/me/account', allow_redirects = False, headers = headers)
        if response.status != 200:
            return JSONResponse(status_code = 404, content = '')
     
        return templates.TemplateResponse(
            'account-info.html', {'request': request, 'user' : await response.json()}
        )   
    
        
    

@router.get(path = '/account', summary = 'Информация о пользователе')
async def user_account(request : Request) -> HTMLResponse:
    return templates.TemplateResponse(
        'account.html', {'request': request}
    )
    
    
    
    
@router.get(path = '/bucket-info', summary = 'Корзина')
async def bucket_info(request : Request) -> HTMLResponse:
    
    headers = {}
    if request.headers.get('Authorization') is not None:
        headers['Authorization'] = request.headers.get('Authorization')
        
    async with ClientSession() as session:
        response = await session.get('http://user-service:8000/api/me/bucket', allow_redirects = False, headers = headers)

        if response.status != 200:
            return JSONResponse(status_code = 404, content = '')
     
        return templates.TemplateResponse(
            'bucket-info.html', {'request': request, 'bucket' : await response.json()}
        )   
    
        
        
@router.get(path = '/bucket', summary = 'Корзина')
async def user_buclet(request : Request) -> HTMLResponse:
    return templates.TemplateResponse(
        'bucket.html', {'request': request}
    )

        
    
@router.get(path = '/orders-info', summary = 'Заказы')
async def orders_info(request : Request) -> HTMLResponse:
    
    headers = {}
    if request.headers.get('Authorization') is not None:
        headers['Authorization'] = request.headers.get('Authorization')
        
    async with ClientSession() as session:
        response = await session.get('http://user-service:8000/api/me/orders', allow_redirects = False, headers = headers)

        if response.status != 200:
            return JSONResponse(status_code = 404, content = '')
     
        return templates.TemplateResponse(
            'orders-info.html', {'request': request, 'orders' : await response.json()}
        )   
    
        
        
@router.get(path = '/orders', summary = 'Заказы')
async def user_buclet(request : Request) -> HTMLResponse:
    return templates.TemplateResponse(
        'orders.html', {'request': request}
    )
    
        
        
            

    
    

