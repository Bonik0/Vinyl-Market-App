from pydantic import Field, ConfigDict, EmailStr, AliasChoices, PositiveInt
from .BaseModel import BaseModel
from core.models.postgres import UserRole
from core.models.postgres import MIN_VARCHAR_VALUE, MAX_VARCHAR_VALUE



class NonPrivateUserInfo(BaseModel):
    username : str = Field(min_length = 5, max_length = MAX_VARCHAR_VALUE, description = 'Ник пользователя')
    
    model_config = ConfigDict(title = 'Короткая инормация о пользователе')
 

class PrivateUserInfo(NonPrivateUserInfo):
    first_name : str = Field(min_length = MIN_VARCHAR_VALUE, max_length = MAX_VARCHAR_VALUE, xdescription = 'Имя пользователя')
    last_name : str = Field(min_length = MIN_VARCHAR_VALUE, max_length = MAX_VARCHAR_VALUE, description = 'Фамилия пользователя')
    email : EmailStr = Field(min_length = MIN_VARCHAR_VALUE, max_length = MAX_VARCHAR_VALUE, description = 'Почта пользователя')   
    

class NonPrivateUserInfoOut(NonPrivateUserInfo):
    role : UserRole = Field(default = UserRole.user)
    user_id : PositiveInt = Field(validation_alias = AliasChoices('id', 'user_id'))
    



class PrivateUserInfoOut(NonPrivateUserInfoOut, PrivateUserInfo):
    pass
    