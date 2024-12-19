from core.dao import PostgresDAO, AsyncSession
from sqlalchemy import text
from core.schemas import VinylRecordID, UserActionOut, SuccessUserActionStatusType, OrderInfoOut, OrderListOut
from pydantic import PositiveInt
from sqlalchemy.exc import DBAPIError
from .errors import VinylZeroQuantityError, OrderCancelError


class UserOrdersDAO(PostgresDAO):
    
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_user_orders_by_user_id(cls,
                                        session : AsyncSession,
                                        user_id : PositiveInt
                                    ) -> OrderListOut:
        query_for_select_orders =   """
                                    SELECT order_id, user_id, status, created_at, vinyl_record_id, seller_id, release_date, title, UPC, image_url, price
                                    FROM vinyl_record_orders
                                    WHERE user_id = :user_id;
                                    """
        
        order_items = await session.execute(text(query_for_select_orders), {'user_id' : user_id})
        
        return OrderListOut(items = [OrderInfoOut.model_validate(item._asdict()) for item in order_items.all()])
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def create_order(cls,
                            session : AsyncSession,
                            user_id : PositiveInt,
                            vinyl_record_id : VinylRecordID
                        ) -> UserActionOut:
        
        query_for_create_order =    """
                                    INSERT INTO orders (user_id, vinyl_record_id)
                                    VALUES (:user_id, :vinyl_record_id)
                                    RETURNING id;
                                    """
        
        try:
            await session.scalar(text(query_for_create_order), {'user_id' : user_id, 'vinyl_record_id' : vinyl_record_id})
        except DBAPIError:
            raise VinylZeroQuantityError
        
        return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_INSERT)
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def cancel_order(cls,
                            session : AsyncSession,
                            user_id : PositiveInt,
                            order_id : PositiveInt
                        ) -> UserActionOut:
        query_for_cancel_order = """
                                    UPDATE orders
                                    SET status = 'canceled'
                                    WHERE id = :order_id AND user_id = :user_id AND status != 'canceled' AND status != 'delivered'
                                    RETURNING id;
                                 """
                                 
        
        is_canceled = await session.scalar(text(query_for_cancel_order), {'user_id' : user_id, 'order_id' : order_id})
        
        if is_canceled is None:
            raise OrderCancelError
        
        return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)
        
        
        
                                    
        
        
        
    