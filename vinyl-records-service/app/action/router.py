from fastapi import APIRouter, Path, Request
from core.schemas import VinylRecordID
from .dao import VinylRecordActionDAO
from .schemas import VinylRecordWithSellerOut
from .errors import VinylRecordException
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from aiohttp import ClientSession


router = APIRouter(
                    prefix = '/vinyl-record',
                    tags = ['Пластинки'],
                    responses = VinylRecordException.get_responses_schemas()
                )


templates = Jinja2Templates(directory = './app/templates')



@router.get(path = '/{vinyl_record_id}', summary = 'Получить пластинку по ID')
async def get_vinyl_record_by_id(vinyl_record_id : Annotated[VinylRecordID, Path()]) -> VinylRecordWithSellerOut:
    return await VinylRecordActionDAO.get_vinyl_record_by_id(vinyl_record_id)


