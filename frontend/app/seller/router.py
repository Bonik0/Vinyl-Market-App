from fastapi import APIRouter, Depends, Request, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from core.schemas import VinylRecordOut, VinylRecordID
from typing import Annotated
from aiohttp import ClientSession
from math import ceil
import logging



templates = Jinja2Templates(directory = './app/seller/templates')



router = APIRouter(
                    prefix = '/seller',
                    tags = ['Продавец']
                )



@router.get(path = '/orders-info', summary = 'Заказы')
async def orders_info(request : Request) -> HTMLResponse:
    headers = {}
    if request.headers.get('Authorization') is not None:
        headers['Authorization'] = request.headers.get('Authorization')
        
    async with ClientSession() as session:
        response = await session.get('http://seller-service:8000/api/seller/orders', allow_redirects = False, headers = headers)
        if response.status != 200:
            return JSONResponse(status_code = 400, content = f'{response.status}')
     
        return templates.TemplateResponse(
            'orders-info.html', {'request': request, 'orders' : await response.json()}
        )   
    
        
        
@router.get(path = '/orders', summary = 'Заказы')
async def orders(request : Request) -> HTMLResponse:
    return templates.TemplateResponse(
        'orders.html', {'request': request}
    )
    
    
    
    
@router.get(path = '/vinyl-records-info', summary = 'Пластинки')
async def vinyl_records_info(request : Request) -> HTMLResponse:
    headers = {}
    if request.headers.get('Authorization') is not None:
        headers['Authorization'] = request.headers.get('Authorization')
        
    async with ClientSession() as session:
        response = await session.get('http://seller-service:8000/api/seller/vinyl-records', allow_redirects = False, headers = headers)
        if response.status != 200:
            return JSONResponse(status_code = 400, content = f'{response.status}')
     
        return templates.TemplateResponse(
            'vinyl-records-info.html', {'request': request, 'vinyl_records' : await response.json()}
        )   
    
        
        
@router.get(path = '/vinyl-records', summary = 'Пластинки')
async def vinyl_records(request : Request) -> HTMLResponse:
    return templates.TemplateResponse(
        'vinyl-records.html', {'request': request}
    )
    
    
    
    
    

    
@router.get(path = '/vinyl-records/create-info', summary = 'Создать пластинку')
async def create_vinyl_records_info(request : Request) -> HTMLResponse:
    headers = {}
    if request.headers.get('Authorization') is not None:
        headers['Authorization'] = request.headers.get('Authorization')
        
    async with ClientSession() as session:
        response = await session.get('http://user-service:8000/api/me/account', allow_redirects = False, headers = headers)
        if response.status != 200:
            return JSONResponse(status_code = 400, content = f'{response.status}')
        
        response = await response.json()
        
        if response['role'] != 'seller':
             return JSONResponse(status_code = 400, content = f'not seller')
            
     
        return templates.TemplateResponse(
            'create-info.html', {'request': request}
        )   
    
        
        
        
        
        
@router.get(path = '/vinyl-records/create', summary = 'Создать пластинку')
async def create_vinyl_records_info(request : Request) -> HTMLResponse:
     return templates.TemplateResponse(
        'create.html', {'request': request}
    )
    
        
        
        
        
        
           
        
        
        
@router.get(path = '/vinyl-records/{vinyl_record_id}/update-info', summary = 'Обновить пластинку')
async def update_vinyl_records(request : Request, vinyl_record_id : Annotated[VinylRecordID, Path()]) -> HTMLResponse:
    headers = {}
    if request.headers.get('Authorization') is not None:
        headers['Authorization'] = request.headers.get('Authorization')
        
    async with ClientSession() as session:
        response = await session.get('http://seller-service:8000/api/seller/vinyl-records', allow_redirects = False, headers = headers)
        if response.status != 200:
            return JSONResponse(status_code = 400, content = f'{response.status}')
        
        response = await response.json()

        item = {}
        for item in response['items']:
            if item['id'] == vinyl_record_id:
                item = item
                break
            
        print(item)
     
        return templates.TemplateResponse(
            'update-info.html', {'request': request, 'item' : item}
        )
    
    
    

@router.get(path = '/vinyl-records/{vinyl_record_id}/update', summary = 'Обновить пластинку')
async def update_vinyl_records(request : Request, vinyl_record_id : Annotated[VinylRecordID, Path()]) -> HTMLResponse:
    return templates.TemplateResponse(
        'update.html', {'request': request}
    )
    

    
    

    