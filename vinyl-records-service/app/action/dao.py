from core.dao import PostgresDAO, AsyncSession
from sqlalchemy import text
from core.schemas import VinylRecordID, SellerInfoOut
from .schemas import VinylRecordWithSellerOut
import asyncio
from .errors import IncorrectIDError


class VinylRecordActionDAO(PostgresDAO):
    
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_vinyl_record_by_id(cls, session : AsyncSession, vinyl_record_id : VinylRecordID) -> VinylRecordWithSellerOut:
        query_select_for_genres = """
                                    SELECT title
                                    FROM genres
                                    WHERE id IN (
                                        SELECT genre_id
                                        FROM genre_assotiation 
                                        WHERE vinyl_record_id = :vinyl_record_id
                                    );
                                """
                                
        query_select_for_artists = """
                                    SELECT name 
                                    FROM artists
                                    WHERE id IN (
                                        SELECT artist_id
                                        FROM artist_assotiation
                                        WHERE vinyl_record_id = :vinyl_record_id
                                    );
                                    """
        query_for_select_vinyl_record = """
                                        SELECT id, quantity, seller_id, release_date, title, UPC, image_url, price
                                        FROM vinyl_records
                                        WHERE id = :vinyl_record_id;
                                        """
        query_for_select_seller =   """
                                    SELECT user_id, phone_number, city, country
                                    FROM sellers
                                    WHERE user_id = :user_id;
                                    """
        
        
        
        vinyl_record = await session.execute(text(query_for_select_vinyl_record), {'vinyl_record_id' : vinyl_record_id}) 
        vinyl_record = vinyl_record.one_or_none()
        
        if vinyl_record is None:
            raise IncorrectIDError
        
        vinyl_record = vinyl_record._asdict()
                    
        genres, artists, seller = await asyncio.gather(
                                        session.scalars(text(query_select_for_genres), {'vinyl_record_id' : vinyl_record_id}),
                                        session.scalars(text(query_select_for_artists), {'vinyl_record_id' : vinyl_record_id}),
                                        session.execute(text(query_for_select_seller), {'user_id' : vinyl_record['seller_id']})
                                    )
        
        return VinylRecordWithSellerOut(**vinyl_record,
                                        genres = genres.all(),
                                        artists = artists.all(),
                                        seller = SellerInfoOut.model_validate(seller.one()._asdict())
                                    )
        
        
