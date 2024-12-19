from core.schemas import BaseModel, VinylRecordPreviewOut
from pydantic import Field, PositiveInt, computed_field
from fastapi import Query
from typing import Annotated
from core.models.postgres import MAX_VARCHAR_VALUE, MIN_VARCHAR_VALUE
from math import ceil


class SearchQueryIn:
    
    
    def __init__(
                self, 
                text : Annotated[str | None, Query(min_length = MIN_VARCHAR_VALUE, max_length = MAX_VARCHAR_VALUE, description = 'Поиск по названию')] = None,
                artist : Annotated[str | None, Query(min_length = MIN_VARCHAR_VALUE, max_length = MAX_VARCHAR_VALUE, description = 'Поиск по исполнителю')] = None,
                genre : Annotated[str | None, Query(min_length = MIN_VARCHAR_VALUE, max_length = MAX_VARCHAR_VALUE, description = 'Поиск по жанру')] = None,
                page : Annotated[PositiveInt, Query(le = 40, description = 'Страница выдачи')] = 1,
                perpage : Annotated[PositiveInt, Query(le = 250, description = 'Количество товаров на странице')] = 25
            ) -> None:
        self.text = text
        self.artist = artist
        self.genre = genre
        self.page = page
        self.perpage = perpage
    
    @property
    def offset(self) -> PositiveInt:
        return (self.page - 1) * self.perpage


    def to_dict(self) -> dict[str, int | str | None]:
        return {
            'text' : self.text,
            'artist' : self.artist,
            'genre' : self.genre,
            'offset' : self.offset,
            'limit' : self.perpage
        }
        
    def to_params(self) -> dict[str, int | str]:
        params = {}
        for attr, value in self.__dict__.items():
            if value is not None:
                params[attr] = value
        return params
            
        
    def pages(self, items_count : int) -> tuple[int, int]:
        max_page = min(max(self.page + 3, 6), ceil(items_count / self.perpage), 40)
        return max(max_page - 5, 1), max_page
    
        
        
        
class SearchVinylRecordOut(BaseModel):
    items : list[VinylRecordPreviewOut]
    counter : int = Field(ge = 0, description = 'Количесво найденных пластинок')
    
    