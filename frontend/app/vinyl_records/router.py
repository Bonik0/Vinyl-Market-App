from fastapi import APIRouter, Depends, Request, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from core.schemas import VinylRecordOut, VinylRecordID
from typing import Annotated
from aiohttp import ClientSession
from math import ceil



templates = Jinja2Templates(directory = './app/vinyl_records/templates')



router = APIRouter(
                    tags = ['Пластинки']
                )




@router.get(path = '/', summary = 'Главное меню')
async def main_board(request : Request) -> HTMLResponse:
    bucket = {'items' : [], 'counter' : 0}
    query = request.query_params._dict
    async with ClientSession() as session:
        response = await session.get('http://vinyl-records-service:8000/api/search', params = query)
        response = await response.json()
        
        
        
    page = int(query['page']) if query.get('page') is not None else 1
    perpage = int(query['perpage']) if query.get('perpage') is not None else 25
    offset = (page - 1) * perpage
    max_page = min(max(page + 3, 6), ceil(response.get('counter') / perpage), 40)
    min_page = max(max_page - 5, 1)
    
    return templates.TemplateResponse(
        'search.html', {'request': request,
                        'vinyl_records' : response,
                        'offset' : offset,
                        'perpage' : perpage,
                        'page' : page,
                        'max_page' : max_page,
                        'min_page' : min_page
                        }
    )


@router.get(path = '/advanced-search', summary = 'Расширеный поиск')
async def advanced_search(request : Request) -> HTMLResponse:
    return templates.TemplateResponse(
        'advanced_search.html', {'request': request}
    )



@router.get(path = '/vinyl-record/{vinyl_record_id}', summary = 'Получить пластинку по ID')
async def get_vinyl_record_by_id(request : Request, vinyl_record_id : Annotated[int, Path()]) -> HTMLResponse:
    async with ClientSession() as session:
        response = await session.get(f'http://vinyl-records-service:8000/api/vinyl-record/{vinyl_record_id}')
        
    return templates.TemplateResponse(
        'vinyl_record.html', {'request': request, 'vinyl_record' : await response.json()}
    )


    