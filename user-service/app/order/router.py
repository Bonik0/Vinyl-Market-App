from fastapi import APIRouter, Depends, Request, Path
from core.schemas import UserActionOut, VinylRecordID, OrderInfoOut, OrderListOut
from core.services_and_endpoints import endpoints
from typing import Annotated
from .dao import UserOrdersDAO
from .errors import UserOrderException
from pydantic import PositiveInt



router = APIRouter(
                   tags = ['Заказы'],
                   prefix = '/orders',
                   responses = UserOrderException.get_responses_schemas()
                )



@router.get(path = '', summary = 'Заказанные товары')
async def user_orders(request : Request) -> OrderListOut:
    return await UserOrdersDAO.get_user_orders_by_user_id(user_id = request.state.user.user_id)
    
    
    
@router.post(path = '/create/{vinyl_record_id}', summary = 'Заказазать товар')
async def create_order(request : Request, vinyl_record_id : Annotated[VinylRecordID, Path()]) -> UserActionOut:
    return await UserOrdersDAO.create_order(request.state.user.user_id, vinyl_record_id)
    
    
    
@router.post(path = '/cancel/{order_id}', summary = 'отменить заказ')
async def cancel_order(request : Request, order_id : Annotated[PositiveInt, Path()]) -> UserActionOut:
    return await UserOrdersDAO.cancel_order(request.state.user.user_id, order_id)
    