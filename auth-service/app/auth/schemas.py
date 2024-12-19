from pydantic import Field, ConfigDict, field_serializer, EmailStr, field_validator
from core.schemas import BaseModel, PrivateUserInfo
from core.models.postgres import MAX_VARCHAR_VALUE, MIN_VARCHAR_VALUE
from hashlib import sha256
import re


class UserCredentialsIn(BaseModel):
    
    password : str = Field(serialization_alias = 'hash_password', min_length = 5, max_length = MAX_VARCHAR_VALUE, description = 'Пароль')
    
    @field_serializer('password')
    @classmethod
    def password_serialize(cls, password : str) -> str:
        return sha256(str.encode(password)).hexdigest()




class UserLoginCredentialsIn(UserCredentialsIn):
    username_or_email : str | EmailStr = Field(min_length = 5, max_length = MAX_VARCHAR_VALUE, description = 'Никнейм или емейл')
    
    model_config = ConfigDict(title = 'Вход в аккаут')
    



class UserRegistrationCredentialsIn(PrivateUserInfo, UserCredentialsIn):
    
    model_config = ConfigDict(title = 'Создание аккаута')
    
    
    @field_validator('username', mode = 'after')
    @classmethod
    def check_username_is_not_like_email(cls, username : str) -> str:
        if re.match(r'^\S+@\S+\.\S+$', username):
            raise ValueError('username like email')
        return username
        
        
        
        
class RefreshTokenIn(BaseModel):
    
    refresh_token : str = Field(min_length = MIN_VARCHAR_VALUE, description = 'refresh_token')
    
    model_config = ConfigDict(title = 'Форма для обновления токенов')
    
    

    

