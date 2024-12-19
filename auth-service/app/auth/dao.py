from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, RefreshTokenIn
from core.dependencies.JWTToken import TokenValidation, JWTTokenDAO, IssuedJWTTokensOut, IssuedJWTTokenPayloadOut
from sqlalchemy.ext.asyncio import AsyncSession
from core.dao import PostgresDAO
from sqlalchemy import text, Row
from .errors import (
                    UsernameOccupiedError,
                    EmailOccupiedError,
                    AuthException,
                    InvalidPasswordError,
                    InvalidUsernameOrEmailError,
                    RepeatRegistratesellerError
                )
from core.schemas import NonPrivateUserInfoOut, SellerInfoIn
from typing import Any
from core.models.postgres import UserRole



class AuthDAO(PostgresDAO):
    
    @classmethod
    async def get_user_by_email_or_username(cls,
                                            session : AsyncSession,
                                            username : str,
                                            email : str
                                        ) -> Row[Any] | None:
        
        query_for_find_user =   """
                                SELECT id, username, email, hash_password, role FROM users WHERE email = :email
                                UNION 
                                SELECT id, username, email, hash_password, role FROM users WHERE username = :username;
                                """
        
        user = await session.execute(text(query_for_find_user), {'username' : username, 'email' : email})
        
        return user.one_or_none()
      
          
    
    @classmethod
    async def get_user_with_same_credentials(cls,
                                               session : AsyncSession,
                                               user_credentials : UserRegistrationCredentialsIn
                                            ) -> AuthException | None:
        
        user_with_same_credentials_row = await cls.get_user_by_email_or_username(session, user_credentials.username, user_credentials.email)
        if user_with_same_credentials_row is None:
            return None
        
        user_with_same_credentials_dict = user_with_same_credentials_row._asdict()
        
        if user_credentials.email == user_with_same_credentials_dict['email']:
            return EmailOccupiedError
        
        return UsernameOccupiedError
    
    
    
    @classmethod
    async def get_user_with_logining_credentials(cls, 
                                                  session : AsyncSession,
                                                  user_credentials : UserLoginCredentialsIn,
                                                ) -> tuple[dict[str, int | str] | None, AuthException | None]:
                    
        user_row = await cls.get_user_by_email_or_username(session, user_credentials.username_or_email, user_credentials.username_or_email)
        if user_row is None:
            return None, InvalidUsernameOrEmailError
        
        user_dict = user_row._asdict()
        
        if user_dict['hash_password'] != UserLoginCredentialsIn.password_serialize(user_credentials.password):
            return None, InvalidPasswordError
        
        return user_dict, None
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def registrate(cls,
                         session : AsyncSession, 
                         user_credentials : UserRegistrationCredentialsIn
                        ) -> IssuedJWTTokensOut:
        query_for_new_user = 'INSERT INTO users (username, first_name, last_name, email, hash_password) VALUES (:username, :first_name, :last_name, :email, :hash_password) RETURNING id;'
        
        error = await cls.get_user_with_same_credentials(session, user_credentials)
        
        if error is not None:
            raise error
        
        user_id = await session.scalar(text(query_for_new_user), user_credentials.model_dump())
        
        return await JWTTokenDAO.generate_and_save_new_tokens_by_user_id(session, 
                                                                        NonPrivateUserInfoOut(
                                                                                username = user_credentials.username,
                                                                                user_id = user_id
                                                                            )
                                                                    )
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def login(cls,
                    session : AsyncSession,
                    user_credentials : UserLoginCredentialsIn
                ) -> IssuedJWTTokensOut:
            
        loggining_user, error = await cls.get_user_with_logining_credentials(session, user_credentials)
        
        if error is not None:
            raise error
        
        return await JWTTokenDAO.generate_and_save_new_tokens_by_user_id(session, NonPrivateUserInfoOut.model_validate(loggining_user))
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def seller_registrate(cls,
                                session : AsyncSession,
                                token_payload : IssuedJWTTokenPayloadOut,
                                seller_credentials : SellerInfoIn
                            ) -> IssuedJWTTokensOut:
        
        if token_payload.role != UserRole.user:
            raise RepeatRegistratesellerError
        
        query_for_insert_new_seller =   """
                                        INSERT INTO sellers (user_id, phone_number, city, country) VALUES (:user_id, :phone_number, :city, :country)
                                        """
        await JWTTokenDAO.delete_all_user_tokens_by_user_id(session, token_payload.user_id)                        
        await session.execute(text(query_for_insert_new_seller), seller_credentials.model_dump() | {'user_id' : token_payload.user_id})
        
        return await JWTTokenDAO.generate_and_save_new_tokens_by_user_id(session, 
                                                                        NonPrivateUserInfoOut(
                                                                                            username = token_payload.username,
                                                                                            user_id = token_payload.user_id,
                                                                                            role = UserRole.seller              
                                                                        )
                                                                )
    
        
        
        
        
        
            
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True, ignore_http_errors = True)
    async def update_tokens(cls,
                            session : AsyncSession,
                            refresh_token : RefreshTokenIn
                        ) -> IssuedJWTTokensOut:
        refresh_token_data = TokenValidation.check_refresh_token(refresh_token.refresh_token)    
        _, error = await JWTTokenDAO.delete_user_tokens_by_device_id(session, refresh_token_data.device_id)
        
        if error is not None:
            await JWTTokenDAO.delete_all_user_tokens_by_user_id(session, refresh_token_data.user_id)
            raise error
        
        return await JWTTokenDAO.generate_and_save_new_tokens_by_user_id(session, NonPrivateUserInfoOut.model_validate(refresh_token_data))
            
                                  
      
            
    
    
        
        
            
        
        
        
            
            