from pydantic import Field, ConfigDict, field_validator, PositiveInt, computed_field
from .BaseModel import BaseModel
from .vinyl_record import VinylRecordPreview, VinylRecordID
from core.models.postgres import MIN_VARCHAR_VALUE, OrderStatus, MAX_INT_OR_FLOAT_VALUE
from datetime import datetime



class OrderInfoOut(VinylRecordPreview):
    vinyl_record_id : VinylRecordID = Field(description = 'ID пластинки')
    seller_id : PositiveInt = Field(le = MAX_INT_OR_FLOAT_VALUE, description = 'ID продавца')
    created_at : datetime = Field(description = 'Время создания заказа')
    order_id : PositiveInt = Field(le = MAX_INT_OR_FLOAT_VALUE, description = 'ID заказа')
    status : OrderStatus = Field(description = 'Статус заказа')

    model_config = ConfigDict(title = 'Заказ информация')
    
    @computed_field
    @property
    def local_link(self) -> str:
        return f'/vinyl-record/{self.vinyl_record_id}'
    
    
    @computed_field
    @property
    def created_at_str(self) -> str:
        return self.created_at.strftime('%d/%m/%Y %H:%M')
    
    
class OrderListOut(BaseModel):
    items : list[OrderInfoOut]
    
    @computed_field(description = 'Количесво заказов')
    @property
    def counter(self) -> int:
        return len(self.items)
    
