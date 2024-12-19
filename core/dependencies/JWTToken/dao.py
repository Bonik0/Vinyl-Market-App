from .schemas import IssuedJWTTokensOut
from .errors import TokenRevokedError, JWTException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .JWTToken import JWTToken
from core.dao.PostgresDAO import PostgresDAO, AsyncSession
from core.schemas.user import PrivateUserInfoOut
from uuid import UUID




class JWTTokenDAO(PostgresDAO):
    
    
    @classmethod
    @PostgresDAO.get_session()
    async def check_token_is_remove(cls, session : AsyncSession, jti : str) -> None:
        
        query_for_select_token = 'SELECT jti FROM issued_jwt_tokens WHERE jti = :jti;'
        token_db = await session.execute(text(query_for_select_token), {'jti' : jti})
        
        if token_db.one_or_none() is None:
            raise TokenRevokedError
    
        
        
    @classmethod
    async def delete_user_tokens_by_device_id(
                                            cls,
                                            session : AsyncSession,
                                            device_id : str
                                        ) -> tuple[int | None, JWTException | None]:
        query_for_delete_tokens =   """
                                    DELETE FROM issued_jwt_tokens WHERE device_id = :device_id RETURNING user_id;
                                    """
        
        user_id = await session.execute(text(query_for_delete_tokens), {'device_id' : device_id})
        
        user_id = user_id.first()
        
        if user_id is None:
            return None, TokenRevokedError
        
        return user_id, None
    
    
    @classmethod
    async def delete_all_user_tokens_by_user_id(cls,
                                                session : AsyncSession,
                                                user_id : int
                                            ) -> None:
        query_for_delete_all_tokens =   """
                                        DELETE FROM issued_jwt_tokens WHERE user_id = :user_id;
                                        """

        await session.execute(text(query_for_delete_all_tokens), {'user_id' : user_id})
        
        
        
    @classmethod
    async def generate_and_save_new_tokens_by_user_id(
                                                cls,
                                                session : AsyncSession,
                                                payload : PrivateUserInfoOut,
                                            ) -> IssuedJWTTokensOut:
        
        new_tokens_with_data = JWTToken.generate_tokens(payload)
        query_for_insert_tokens = 'INSERT INTO issued_jwt_tokens (jti, device_id, user_id) VALUES (:jti, :device_id, :user_id);'
        await session.execute(text(query_for_insert_tokens), [token_data.model_dump() | {'user_id' : payload.user_id} for token_data in new_tokens_with_data.data])
        return new_tokens_with_data.tokens
        
    
        
    
        
        
             
            