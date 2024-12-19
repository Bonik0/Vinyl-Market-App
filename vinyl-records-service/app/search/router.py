from fastapi import APIRouter, Depends
from .dao import SearchVinylRecordDAO
from .schemas import SearchQueryIn, SearchVinylRecordOut
from typing import Annotated


router = APIRouter(
                    tags = ['Пластинки']
                )




@router.get(path = '/search', summary = 'Поиск')
async def get_vinyl_record_by_id(query : Annotated[SearchQueryIn, Depends()]) -> SearchVinylRecordOut:
    return await SearchVinylRecordDAO.get_vinyl_records_by_user_filters(query)









    
