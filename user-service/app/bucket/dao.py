from core.dao import PostgresDAO, AsyncSession
from sqlalchemy import text
from core.schemas import VinylRecordPreviewOut, VinylRecordID, UserActionOut, SuccessUserActionStatusType
from .schemas import BucketInfoOut
from pydantic import PositiveInt
from sqlalchemy.exc import IntegrityError
from .errors import BucketInsertError, VinylRecordNotPresentError




class BucketDAO(PostgresDAO):
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def insert_vinyl_record_in_bucket(cls,
                                            session : AsyncSession,
                                            user_id : PositiveInt,
                                            vinyl_record_id : VinylRecordID
                                        ) -> UserActionOut:
        query_for_insert_vinyl_order =  """
                                        INSERT INTO bucket (user_id, vinyl_record_id) VALUES (:user_id, :vinyl_record_id);
                                        """
        
        try:
            await session.execute(text(query_for_insert_vinyl_order), {'user_id' : user_id, 'vinyl_record_id' : vinyl_record_id})
        except IntegrityError:
            raise BucketInsertError
            
        return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_INSERT)
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def delete_vinyl_record_in_bucket(cls,
                                            session : AsyncSession,
                                            user_id : PositiveInt,
                                            vinyl_record_id : VinylRecordID
                                        ) -> UserActionOut:
        query_for_delete_vinyl_record = """
                                        DELETE FROM bucket
                                        WHERE user_id = :user_id AND vinyl_record_id = :vinyl_record_id
                                        RETURNING vinyl_record_id;
                                        """
        
        is_delete = await session.scalar(text(query_for_delete_vinyl_record), {'user_id' : user_id, 'vinyl_record_id' : vinyl_record_id})

        if is_delete is None:
            raise VinylRecordNotPresentError
    
        return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)
    
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_user_bucket_by_user_id(cls,
                                        session : AsyncSession,
                                        user_id : PositiveInt
                                    ) -> BucketInfoOut:
        
        query_for_select_bucket_items = """
                                        SELECT id, quantity, seller_id, release_date, title, UPC, image_url, price
                                        FROM vinyl_records
                                        WHERE id IN (
                                                SELECT vinyl_record_id FROM bucket_ids
                                                WHERE user_id = :user_id
                                            )
                                        ORDER BY array_position(
                                            ARRAY(
                                                SELECT vinyl_record_id FROM bucket_ids
                                                WHERE user_id = :user_id
                                            ), id);
                                        """
                                        
        bucket_items = await session.execute(text(query_for_select_bucket_items), {'user_id' : user_id})
        
        return BucketInfoOut(items = [VinylRecordPreviewOut.model_validate(item._asdict()) for item in bucket_items.all()])
        