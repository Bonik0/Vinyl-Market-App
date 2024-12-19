from core.dao import AsyncSession, PostgresDAO
from core.schemas import VinylRecordPreviewOut, VinylRecordID
from sqlalchemy import text, Row
from .schemas import SearchQueryIn, SearchVinylRecordOut




class SearchVinylRecordDAO(PostgresDAO):
    
    
    @classmethod
    def get_query_for_vinyl_ids_by_genre(cls) -> str:
        
        query_for_select_vinyl_ids = """
                                       SELECT DISTINCT vinyl_record_id
                                       FROM genre_assotiation
                                       WHERE genre_id IN (
                                           SELECT id 
                                           FROM genres
                                           WHERE title LIKE '%' || :genre || '%'
                                       )
                                    """
        return query_for_select_vinyl_ids
    
    
    @classmethod
    def get_query_for_vinyl_ids_by_artist(cls) -> str:
        
        query_for_select_vinyl_ids = """
                                    SELECT DISTINCT vinyl_record_id
                                    FROM artist_assotiation
                                    WHERE artist_id IN (
                                            SELECT id
                                            FROM artists
                                            WHERE name LIKE '%' || :artist || '%'
                                        )
                                    """
        return query_for_select_vinyl_ids                                         
    
    @classmethod
    @PostgresDAO.get_session()
    async def get_vinyl_records_by_user_filters(
                                                cls,
                                                session : AsyncSession,
                                                query : SearchQueryIn
                                            ) -> SearchVinylRecordOut:
        
        final_select_query : str =  """
                                    SELECT id, quantity, seller_id, release_date, title, UPC, image_url, price
                                    FROM vinyl_records
                                    """
        page_filter : str =     """
                                    ORDER BY id DESC
                                    LIMIT :limit
                                    OFFSET :offset;
                                """
        query_for_select_count_results = """
                                            SELECT COUNT(id) FROM  
                                         """ 
        query_where : list[str] = ['quantity > 0']
        query_filter_for_artist_and_genre : list[str] = []
        
        
        if query.genre is not None:
            query_filter_for_artist_and_genre.append(cls.get_query_for_vinyl_ids_by_genre())
            
            
        if query.artist is not None:
            query_filter_for_artist_and_genre.append(cls.get_query_for_vinyl_ids_by_artist())
            
            
        if query.text is not None:
            query_where.append("title LIKE '%' || :text || '%'")
        
        
        if len(query_filter_for_artist_and_genre) != 0:
            query_where.append(f"id = ANY({('INTERSECT').join(query_filter_for_artist_and_genre)})")
        
        final_query_without_fiter = f'{final_select_query} WHERE {" AND ".join(query_where)}'
            
        query_for_select_count_results = f'{query_for_select_count_results} ({final_query_without_fiter}) AS search'
            
        final_select_query = final_query_without_fiter + page_filter
        
        vinyl_records = await session.execute(text(final_select_query), query.to_dict())
        
        counter = await session.scalar(text(query_for_select_count_results), query.to_dict())
        
        return SearchVinylRecordOut(
                                    items = [VinylRecordPreviewOut.model_validate(vinyl_record._asdict()) for vinyl_record in vinyl_records],
                                    counter = counter
                                )
            
            

            
        
        
        
        
        
    