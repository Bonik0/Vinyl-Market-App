from fastapi import APIRouter, Depends, Request, Path
from core.schemas import PrivateUserInfoOut, UserActionOut, VinylRecordID
from .dao import BucketDAO
from core.services_and_endpoints import endpoints
from .schemas import BucketInfoOut
from typing import Annotated
from .errors import BucketException


router = APIRouter(
                   tags = ['Корзина'],
                   prefix = '/bucket',
                   responses = BucketException.get_responses_schemas()
                )



@router.get(path = '', summary = 'Товары в корзине')
async def user_bucket(request : Request) -> BucketInfoOut:
    return await BucketDAO.get_user_bucket_by_user_id(user_id = request.state.user.user_id)
    
    
@router.post(path = '/delete/{vinyl_record_id}', summary = 'Удалить товар')
async def delete_vinyl_from_bucket(request : Request, vinyl_record_id : Annotated[VinylRecordID, Path()]) -> UserActionOut:
    return await BucketDAO.delete_vinyl_record_in_bucket(request.state.user.user_id, vinyl_record_id)


@router.post(path = '/create/{vinyl_record_id}', summary = 'Добавить товар')
async def insert_vinyl_from_bucket(request : Request, vinyl_record_id : Annotated[VinylRecordID, Path()]) -> UserActionOut:
    return await BucketDAO.insert_vinyl_record_in_bucket(request.state.user.user_id, vinyl_record_id)

    