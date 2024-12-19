from pydantic import Field, ConfigDict, PositiveInt, PositiveFloat, AnyHttpUrl, field_validator, computed_field
from .BaseModel import BaseModel
from typing import Annotated
import annotated_types
from datetime import datetime
from core.models.postgres import MIN_VARCHAR_VALUE, MAX_BIG_INT_VALUE, MAX_INT_OR_FLOAT_VALUE, MAX_SMALL_INT_VALUE, MAX_VARCHAR_VALUE



MAX_VINYL_RECORD_ID : int = 10_000_000

VinylRecordID = Annotated[PositiveInt, annotated_types.Le(MAX_VINYL_RECORD_ID)]


class VinylRecordIDInfo(BaseModel):
    id : VinylRecordID = Field(description = 'ID пластинки')
    seller_id : PositiveInt = Field(le = MAX_INT_OR_FLOAT_VALUE, description = 'ID продавца')
    
    @computed_field
    @property
    def local_link(self) -> str:
        return f'/vinyl-record/{self.id}'
    
    

class VinylRecordQuantity(BaseModel):
    quantity : int = Field(ge = 0, le = MAX_SMALL_INT_VALUE, description = 'КОличество пластинок')
    
    
class VinylRecordPreview(BaseModel):
    title : str = Field(min_length = MIN_VARCHAR_VALUE, max_length = MAX_VARCHAR_VALUE, description = 'Название пластинки')
    release_date : datetime = Field(description = 'Дата выхода пластинки')
    upc : PositiveInt = Field(le = MAX_BIG_INT_VALUE, description = 'UPC')
    price : PositiveFloat = Field(le = MAX_INT_OR_FLOAT_VALUE, description = 'Цена в долларах')
    image_url : AnyHttpUrl | None = Field(description = 'Ссылка на изображение пластинки', default = None)
    
    @computed_field
    @property
    def release_date_year(self) -> str:
        return str(self.release_date.year)
    
    @computed_field
    @property
    def release_date_month(self) -> str:
        if self.release_date.month < 10:
            return f'0{self.release_date.month}'
        return str(self.release_date.month)
    
    @computed_field
    @property
    def release_date_day(self) -> str:
        if self.release_date.day < 10:
            return f'0{self.release_date.day}'
        return str(self.release_date.day)
    

    


class VinylRecordPreviewInfo(VinylRecordPreview, VinylRecordQuantity):
    pass



class VinylRecordPreviewOut(VinylRecordPreviewInfo, VinylRecordIDInfo):
    pass 




class VinylRecord(VinylRecordPreviewInfo):
    genres : list[str] = Field(description = 'Жанры')
    artists : list[str] = Field(description = 'Исполнители')
    
    model_config = ConfigDict(title = 'информация о пластинке')
    
    @field_validator('genres', mode = 'after')
    @classmethod
    def validator_genres(cls, genres : list[str]) -> list[str]:

        if any(map(lambda genre : len(genre) < 1 or len(genre) > MAX_VARCHAR_VALUE, genres)):
            raise ValueError('genre too short or too long')
        
        return genres


    @field_validator('artists', mode = 'after')
    @classmethod
    def validator_genres(cls, artists : list[str]) -> list[str]:

        if any(map(lambda artist : len(artist) < 1 or len(artist) > MAX_VARCHAR_VALUE, artists)):
            raise ValueError('artist name too short or too long')
        
        return artists
    
    
    
    
class VinylRecordOut(VinylRecord, VinylRecordIDInfo):
    pass


