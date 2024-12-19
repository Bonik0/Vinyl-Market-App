from fastapi import APIRouter, Request, Path
from core.schemas import VinylRecordPreviewOut, VinylRecordID, UserActionOut, OrderInfoOut, OrderListOut
from typing import Annotated
from .dao import SellerOrdersDAO
from .errors import SellerOrderException
from pydantic import PositiveInt


router = APIRouter(
                    prefix = '/orders',
                    tags = ['Заказы'],
                    responses = SellerOrderException.get_responses_schemas()
               )



@router.get(path = '', summary = 'Заказанные товары')
async def seller_orders(request : Request) -> OrderListOut:
    return await SellerOrdersDAO.get_orders_by_seller_id(request.state.user.user_id)
    

@router.post(path = '/cancel/{order_id}', summary = 'отменить заказ')
async def cancel_order(request : Request, order_id : Annotated[PositiveInt, Path()]) -> UserActionOut:
    return await SellerOrdersDAO.cancel_order(request.state.user.user_id, order_id)
    


@router.post(path = '/next-step/{order_id}', summary = 'Следующий шаг заказа')
async def next_status_order(request : Request, order_id : Annotated[PositiveInt, Path()]) -> UserActionOut:
    return await SellerOrdersDAO.next_step_order_status(request.state.user.user_id, order_id)