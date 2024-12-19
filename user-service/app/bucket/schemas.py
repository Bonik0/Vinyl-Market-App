from core.schemas import VinylRecordPreviewOut, BaseModel
from pydantic import computed_field



class BucketInfoOut(BaseModel):
    items : list[VinylRecordPreviewOut]
    
    @computed_field(description = 'Количесво товара')
    @property
    def counter(self) -> int:
        return len(self.items)
    




