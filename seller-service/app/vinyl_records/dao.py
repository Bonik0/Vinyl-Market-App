from core.dao import AsyncSession, PostgresDAO
from core.schemas import VinylRecordPreviewOut, VinylRecordID, UserActionOut, SuccessUserActionStatusType
from pydantic import PositiveInt
from sqlalchemy import text, Row
from .errors import IncorrectIDError, UniqueVinylRecordError, DeleteVinylRecordError
from .schemas import VinylRecordInfoIn, UpdateVinylRecordInfoIn, SellerVinylRecordsOut
from sqlalchemy.exc import IntegrityError
import asyncio



class SellerVinylRecordDAO(PostgresDAO):
    
    @classmethod
    async def insert_vinyl_record_genres(cls,
                                        session : AsyncSession,
                                        vinyl_record_id : VinylRecordID,
                                        genres : list[str] | None
                                    ) -> None:
        
        if genres is None:
            return None
        
        query_for_insert_new_genre =    """
                                        INSERT INTO genres (title) VALUES (:title) RETURNING id;
                                        """
                                        
                                        
        query_for_insert_assotiation =  """
                                        INSERT INTO genre_assotiation (vinyl_record_id, genre_id)
                                        VALUES (:vinyl_record_id, :genre_id);
                                        """
                                        
        
        query_for_select_genres_id =    """
                                        SELECT id, title 
                                        FROM genres
                                        WHERE title = ANY(:genres);
                                        """
        
        genres_titles = await session.execute(text(query_for_select_genres_id), {'genres' : genres})
        genres_titles = genres_titles.all()
        genres_titles_dict : dict[str, int] = {genre[1] : genre[0] for genre in genres_titles}
        
        
        for genre in genres:
            genre_id = genres_titles_dict.get(genre)
            
            if genre_id is None:
                
                genre_id = await session.scalar(text(query_for_insert_new_genre), {'title' : genre})
                
            
            await session.execute(text(query_for_insert_assotiation), {'vinyl_record_id' : vinyl_record_id, 'genre_id' : genre_id})
            
    
    @classmethod
    async def insert_vinyl_record_artists(cls,
                                        session : AsyncSession,
                                        vinyl_record_id : VinylRecordID,
                                        artists : list[str] | None
                                    ) -> None:
        
        if artists is None:
            return None
        
        query_for_insert_new_artist =   """
                                        INSERT INTO artists (name) VALUES (:name) RETURNING id;
                                        """
                                        
                                        
        query_for_insert_assotiation =  """
                                        INSERT INTO artist_assotiation (vinyl_record_id, artist_id)
                                        VALUES (:vinyl_record_id, :artist_id);
                                        """
                                        
        
        query_for_select_artist_id =    """
                                        SELECT id, name 
                                        FROM artists
                                        WHERE name = ANY(:artists);
                                        """
        
        artists_names = await session.execute(text(query_for_select_artist_id), {'artists' : artists})
        artists_names = artists_names.all()
        artists_names_dict : dict[str, int] = {artist[1] : artist[0] for artist in artists_names}
        
        
        for artist in artists:
            artist_id = artists_names_dict.get(artist)
            
            if artist_id is None:
                
                artist_id = await session.scalar(text(query_for_insert_new_artist), {'name' : artist})
                
            
            await session.execute(text(query_for_insert_assotiation), {'vinyl_record_id' : vinyl_record_id, 'artist_id' : artist_id})
            
    
    
    
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_vinyl_record_by_seller_id(cls, session : AsyncSession, seller_id : PositiveInt) -> list[VinylRecordPreviewOut]:
        query_for_select_vinyl_records_by_seller_id =   """
                                                        SELECT id, quantity, seller_id, release_date, title, UPC, image_url, price
                                                        FROM vinyl_records 
                                                        WHERE seller_id = :seller_id
                                                        ORDER BY id DESC;
                                                        """
                                                        
        vinyl_records = await session.execute(text(query_for_select_vinyl_records_by_seller_id), {'seller_id' : seller_id})
        
        return SellerVinylRecordsOut(items = [VinylRecordPreviewOut(**vinyl_record._asdict()) for vinyl_record in vinyl_records.all()])
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def delete_record_by_id(cls,
                                  session : AsyncSession,
                                  seller_id : PositiveInt,
                                  vinyl_record_id : VinylRecordID
                                ) -> UserActionOut:
        
        
        
        query_for_delete_vinyl_record = """
                                        DELETE FROM vinyl_records 
                                        WHERE id = :vinyl_record_id AND seller_id = :seller_id 
                                        RETURNING id;
                                        """
        query_for_check_orders_status = """
                                        SELECT status
                                        FROM orders
                                        WHERE vinyl_record_id = :vinyl_record_id AND status != 'canceled' AND status != 'delivered'
                                        LIMIT 1;
                                        """
        is_all_orders_close = await session.scalar(text(query_for_check_orders_status),
                                                            {'vinyl_record_id' : vinyl_record_id}
                                                )                               
        is_delete = await session.scalar(text(query_for_delete_vinyl_record),
                                                            {'vinyl_record_id' : vinyl_record_id, 'seller_id' : seller_id}
                                    )
        if is_delete is None:
            raise IncorrectIDError
        
        if is_all_orders_close is not None:
            raise DeleteVinylRecordError
        
        
        return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_DELETE)
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def create_vinyl_record(cls,
                                  session : AsyncSession,
                                  seller_id : PositiveInt,
                                  vinyl_info : VinylRecordInfoIn
                                ) -> VinylRecordID:
        
        query_for_insert_vinyl_record = """
                                        INSERT INTO vinyl_records (quantity, seller_id, release_date, title, UPC, image_url, price)
                                        VALUES (:quantity, :seller_id, :release_date, :title, :upc, :image_url, :price)
                                        RETURNING id;
                                        """
        try:
            vinyl_record_id = await session.scalar(text(query_for_insert_vinyl_record),
                                              (vinyl_info.model_dump(exclude = {'genres', 'artists'}) | {'seller_id' : seller_id})
                                            )
        except IntegrityError:
            raise UniqueVinylRecordError
        
        await asyncio.gather(
                            cls.insert_vinyl_record_genres(session, vinyl_record_id, vinyl_info.genres),
                            cls.insert_vinyl_record_artists(session, vinyl_record_id, vinyl_info.artists)
                        )
        
        
        return vinyl_record_id
    
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def update_vinyl_record_by_id(cls,
                                        session : AsyncSession,
                                        seller_id : PositiveInt,
                                        vinyl_record_id : VinylRecordID,
                                        vinyl_info : UpdateVinylRecordInfoIn
                                    ) -> UserActionOut:
        updated_vinyl_record : VinylRecordID | None
        not_empty_fields = dict((attr, value) for attr, value in vinyl_info.model_dump(exclude = {'genres', 'artists'}).items() if value is not None)
        updated_fields = [f'{attr} = :{attr}' for attr in not_empty_fields.keys()]
        
        query_for_update_vinyl_record = f"""
                                         UPDATE vinyl_records
                                         SET {', '.join(updated_fields)}
                                         WHERE id = :vinyl_record_id AND seller_id = :seller_id
                                         RETURNING id;
                                         """
                                         
        try:
            updated_vinyl_record = await session.scalar(text(query_for_update_vinyl_record),
                                                                (not_empty_fields | {'seller_id' : seller_id, 'vinyl_record_id' : vinyl_record_id})
                                            )
        except IntegrityError:
            raise UniqueVinylRecordError
        
        if updated_vinyl_record is None:
            raise IncorrectIDError
        
        
        await asyncio.gather(
                            cls.insert_vinyl_record_genres(session, vinyl_record_id, vinyl_info.genres),
                            cls.insert_vinyl_record_artists(session, vinyl_record_id, vinyl_info.artists)
                        )
        
        return UserActionOut(status = SuccessUserActionStatusType.SUCCESS_UPDATE)
        
                                        
        