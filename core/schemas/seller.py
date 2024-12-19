from pydantic import Field, ConfigDict, field_validator
from .BaseModel import BaseModel
import re
from core.models.postgres import MIN_VARCHAR_VALUE



class SellerInfo(BaseModel):
    phone_number : str = Field(min_length = MIN_VARCHAR_VALUE, max_length = 15, description = 'Номер телефона')
    city : str = Field(min_length = MIN_VARCHAR_VALUE, max_length = 50, description = 'Город проживания')
    country : str = Field(min_length = MIN_VARCHAR_VALUE, max_length = 50, description = 'Страна проживания')
    
    
    model_config = ConfigDict(title = 'информация о продавце')
    
    
    @field_validator('phone_number', mode = 'before')
    @classmethod
    def phone_number_validate(cls, phone_number : str) -> str:
        
        if re.match(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$', phone_number):
            return phone_number
        
        raise ValueError('incorrect phone number')
    
    
    
class SellerInfoIn(SellerInfo):
    pass


class SellerInfoOut(SellerInfo):
    pass