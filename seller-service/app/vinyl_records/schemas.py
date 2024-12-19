from core.schemas import VinylRecordPreviewInfo, BaseModel, VinylRecordPreviewOut
from pydantic import ConfigDict, Field, field_validator, field_serializer, AnyHttpUrl, PositiveInt, PositiveFloat, computed_field
from datetime import datetime
from core.models.postgres import MAX_VARCHAR_VALUE, MAX_SMALL_INT_VALUE, MAX_BIG_INT_VALUE, MIN_VARCHAR_VALUE, MAX_INT_OR_FLOAT_VALUE




def delete_spaces(string : str) -> str:
    while string.startswith(' '):
        string = string.removeprefix(' ')
    
    while string.endswith(' '):
        string = string.removesuffix(' ')
        
    return string



class SellerVinylRecordInfo(BaseModel):
    genres : list[str] | None = Field(description = 'Жанры пластинки', default = None)
    artists : list[str] | None = Field(description = 'Исполнители', default = None)
    
    @field_serializer('release_date', check_fields = False)
    @classmethod
    def release_date_serialaze(cls, release_date : datetime | None) -> datetime | None:
        if release_date is None:
            return None
        
        return datetime(year = release_date.year, month = release_date.month, day = release_date.day)
    
    
    @field_serializer('image_url', check_fields = False)
    @classmethod
    def image_url_serialaze(cls, image_url : AnyHttpUrl | None) -> str | None:
        if image_url is None:
            return None
        
        return str(image_url)
    
    
    @field_validator('genres', 'artists', mode = 'before', check_fields = False)
    @classmethod
    def validate_genre(cls, string : str) -> list[str] | None:
        if string is None:
            return None
        
        if not isinstance(string, str):
            raise ValueError('inccorect type')
        
        item_list : list[str] = list(map(lambda item : delete_spaces(item), string.split(',')))
        
        if any(map(lambda item : len(item) < MIN_VARCHAR_VALUE or len(item) > MAX_VARCHAR_VALUE or item_list.count(item) > 1, item_list)):
            raise ValueError('genre or artist is too short or too long')
        
        return item_list
    
    
    
    
class UpdateVinylRecordInfo(BaseModel):
    quantity : PositiveInt | None = Field(le = MAX_SMALL_INT_VALUE, description = 'КОличество пластинок', default = None)
    title : str | None = Field(min_length = MIN_VARCHAR_VALUE, max_length = MAX_VARCHAR_VALUE, description = 'Название пластинки', default = None)
    release_date : datetime | None = Field(description = 'Дата выхода пластинки', default = None)
    upc : PositiveInt | None = Field(le = MAX_BIG_INT_VALUE, description = 'UPC', default = None)
    price : PositiveFloat | None = Field(le = MAX_INT_OR_FLOAT_VALUE, description = 'Цена в долларах', default = None)
    image_url : AnyHttpUrl | None = Field(description = 'Ссылка на изображение пластинки', default = None)




class VinylRecordInfoIn(VinylRecordPreviewInfo, SellerVinylRecordInfo):
    pass


class UpdateVinylRecordInfoIn(UpdateVinylRecordInfo, SellerVinylRecordInfo):
    pass


class SellerVinylRecordsOut(BaseModel):
    items : list[VinylRecordPreviewOut]
    
    @computed_field
    @property
    def counter(self) -> int:
        return len(self.items)