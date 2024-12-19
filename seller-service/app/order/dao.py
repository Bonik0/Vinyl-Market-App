from core.dao import PostgresDAO, AsyncSession
from sqlalchemy import text
from core.schemas import VinylRecordID, UserActionOut, SuccessUserActionStatusType, OrderInfoOut, OrderListOut
from pydantic import PositiveInt
from .errors import OrderChengeStatusError


class SellerOrdersDAO(PostgresDAO):
    
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_orders_by_seller_id(cls,
                                        session : AsyncSession,
                                        seller_id : PositiveInt
                                    ) -> OrderListOut:
        
        query_for_select_orders =   """
                                    SELECT order_id, user_id, status, created_at, vinyl_record_id, seller_id, release_date, title, UPC, image_url, price
                                    FROM vinyl_record_orders
                                    WHERE seller_id = :seller_id;
                                    """
        
        order_items = await session.execute(text(query_for_select_orders), {'seller_id' : seller_id})
        
        return OrderListOut(items = [OrderInfoOut.model_validate(item._asdict()) for item in order_items.all()])
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def cancel_order(cls,
                            session : AsyncSession,
                            seller_id : PositiveInt,
                            order_id : PositiveInt
                        ) -> UserActionOut:
        query_for_cancel_order = """
                                    UPDATE orders
                                    SET status = 'canceled'
                                    WHERE id = :order_id 
                                    AND status != 'canceled' 
                                    AND status != 'delivered' 
                                    AND vinyl_record_id = ANY( 
                                                                SELECT id 
                                                                FROM vinyl_records 
                                                                WHERE seller_id = :seller_id
                                                            )
                                    RETURNING id;
                                 """
                                 
        
        is_canceled = await session.scalar(text(query_for_cancel_order), {'seller_id' : seller_id, 'order_id' : order_id})
        
        if is_canceled is None:
            raise OrderChengeStatusError
        
        return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)
    
        
        
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def cancel_order(cls,
                            session : AsyncSession,
                            seller_id : PositiveInt,
                            order_id : PositiveInt
                        ) -> UserActionOut:
        query_for_cancel_order = """
                                    UPDATE orders
                                    SET status = 'canceled'
                                    WHERE id = :order_id 
                                    AND status != 'canceled' 
                                    AND status != 'delivered' 
                                    AND vinyl_record_id = ANY( 
                                                                SELECT id 
                                                                FROM vinyl_records 
                                                                WHERE seller_id = :seller_id
                                                            )
                                    RETURNING id;
                                 """
                                 
        
        is_canceled = await session.scalar(text(query_for_cancel_order), {'seller_id' : seller_id, 'order_id' : order_id})
        
        if is_canceled is None:
            raise OrderChengeStatusError
        
        return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def next_step_order_status(cls,
                                        session : AsyncSession,
                                        seller_id : PositiveInt,
                                        order_id : PositiveInt
                                    ) -> UserActionOut:
        query_for_change_order_status = """
                                           UPDATE orders
                                           SET status = next_order_status(status)
                                           WHERE id = :order_id 
                                           AND status != 'canceled' 
                                           AND status != 'delivered' 
                                           AND vinyl_record_id = ANY( 
                                                                       SELECT id 
                                                                       FROM vinyl_records 
                                                                       WHERE seller_id = :seller_id
                                                                   )
                                           RETURNING id;
                                        """
                                 
        
        is_change = await session.scalar(text(query_for_change_order_status), {'seller_id' : seller_id, 'order_id' : order_id})
        
        if is_change is None:
            raise OrderChengeStatusError
        
        return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_UPDATE)
    
        
        
        
        
        
    
        
        