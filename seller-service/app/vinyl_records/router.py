from fastapi import APIRouter, Request, Path
from core.schemas import VinylRecordPreviewOut, VinylRecordID, UserActionOut
from typing import Annotated
from .dao import SellerVinylRecordDAO
from .errors import SellerVinylRecordException
from .schemas import VinylRecordInfoIn, UpdateVinylRecordInfoIn, SellerVinylRecordsOut





router = APIRouter(
                    prefix = '/vinyl-records',
                    tags = ['Пластинки'],
                    responses = SellerVinylRecordException.get_responses_schemas()
               )





@router.get(path = '', summary = 'Пластники продавца')
async def get_vinyl_records_by_seller(request : Request) -> SellerVinylRecordsOut:
   return await SellerVinylRecordDAO.get_vinyl_record_by_seller_id(request.state.user.user_id)



@router.delete(path = '/{vinyl_record_id}', summary = 'Удалить пластинку')
async def delete_record_by_id(request : Request, vinyl_record_id : Annotated[VinylRecordID, Path()]) -> UserActionOut:
   return await SellerVinylRecordDAO.delete_record_by_id(request.state.user.user_id, vinyl_record_id)



@router.post(path = '/{vinyl_record_id}', summary = 'Обновить пластинку')
async def update_record_by_id(request : Request,
                              vinyl_record_id : Annotated[VinylRecordID, Path()],
                              vinyl_info : UpdateVinylRecordInfoIn
                            ) -> UserActionOut:
   return await SellerVinylRecordDAO.update_vinyl_record_by_id(request.state.user.user_id, vinyl_record_id, vinyl_info)



@router.put(path = '', summary = 'Создать пластинку')
async def create_vinyl_record(request : Request, vinyl_info : VinylRecordInfoIn) -> VinylRecordID:
   return await SellerVinylRecordDAO.create_vinyl_record(request.state.user.user_id, vinyl_info)

