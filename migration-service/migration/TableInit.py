from typing import Any
from alembic import op
from sqlalchemy import Table
from hashlib import sha256
import random
import json
import datetime
from core.models.postgres import OrderStatus


def timetype(date : str):
        return datetime.datetime.strptime(date, '%m/%d/%Y')

class TableInit:
    
    @staticmethod
    def serialize_row(columns_info : dict[str, type], row : str, ignore_rows : list[int] | None = None) -> dict[str, Any]:
        dict_item : dict[str, Any] = {}
        if ignore_rows is None:
            ignore_rows = []
            
        row = row.replace('\n', '')
        for index, (name, type_) in enumerate(columns_info.items()):
            if row == '':
                dict_item[name] = None
                continue
            if index in ignore_rows:
                row = row.split(',', 1)
                if len(row) > 1:
                    _, row = row
                else:
                    row = ''
                continue
            match str(type_):
                case "<class 'str'>":
                    row = row.removeprefix('"').split('",', 1)
                    if len(row) == 2:
                        value, row = row
                    else:
                        value, row = row[0], ''
                    dict_item[name] = str(value).replace('"', '')
                case _:
                    if row.count(',') > 0:
                        value, row = row.split(',', 1)
                    else:
                        value, row = row, ''
                    dict_item[name] = type_(value)       
                    
        return dict_item
    
    
    @staticmethod 
    def parse_data(
                  file_name : str, 
                  columns_info : dict[str, type],
                  ignore_rows : list[int] | None = None
                ) -> list[dict[str, Any]]:
        items : list[dict[str, Any]] = []
        with open(file = file_name, mode = 'r') as file:
            for item in file:
                items.append(TableInit.serialize_row(columns_info, item, ignore_rows))
        return items
    


class DatabaseRandomRowsGenrator:
    
    @staticmethod
    def get_ids(file_name : str) -> list[int]:
        ids : list[int] = []
        with open(file_name, 'r') as file:
            for item in file:
                ids.append(int(item.split(',')[0]))
                
        return ids
    
    
    @classmethod
    def create_random_orders(cls, user_file : str, vinyl_records_file : str, new_file : str) -> None:
        user_ids = cls.get_ids(user_file)
        vinyl_records_ids = cls.get_ids(vinyl_records_file)

        with open(new_file, 'w+') as wf:
            for user_id in user_ids:
                orders_items_count = random.randint(5, 20)
                for _ in range(orders_items_count):
                    vinyl_id = random.choice(vinyl_records_ids)
                    status = random.choice(list(OrderStatus.__members__.keys()))
                    wf.write(f"{user_id},{vinyl_id},{status}\n")
                    
    
    
    @classmethod
    def create_random_bucket_items(cls, user_file : str, vinyl_records_file : str, new_file : str) -> None:
        user_ids = cls.get_ids(user_file)
        vinyl_records_ids = cls.get_ids(vinyl_records_file)
        
        with open(new_file, 'w+') as wf:
            for user_id in user_ids:
                bucket_items_count = random.randint(10, 100)
                vinyl_used_ids : list[int] = []
                for _ in range(bucket_items_count):
                    vinyl_id = random.choice(vinyl_records_ids)
                    while(vinyl_id in vinyl_used_ids):
                        vinyl_id = random.choice(vinyl_records_ids)
                    vinyl_used_ids.append(vinyl_id)
                    
                    wf.write(f"{user_id},{vinyl_id}\n")
        
        
        
        

    @classmethod
    def ctrate_random_seller(cls, file_name : str, new_file_name : str) -> None:
        user_ids : list[int] = cls.get_ids(file_name)
        citys : dict[str, list[dict]] = []
        used_ids : list[int] = []
        citys_str : list[str] = []
        
        with open('migration/versions/csv_data/citys.json', 'r') as cites_file:
            for row in cites_file:
                citys_str.append(row)
           
        citys = json.loads(''.join(citys_str))
        
        with open(new_file_name, 'w+') as wr_file:
            for _ in range(200):
                new_seller_id = random.choice(user_ids)
                while new_seller_id in used_ids:
                    new_seller_id = random.choice(user_ids)
                used_ids.append(new_seller_id)
                city = random.choice(citys['items'])
                numbers = [str(random.randint(0, 9)) for _ in range(11)]
                number_phone = '+' + ''.join(numbers)
                wr_file.write(f'{new_seller_id},"{number_phone}","{city["name"]}","{city["detail"]}"\n')
                
                
    @classmethod
    def delete_none_rows(cls, file_name : str, new_file_name : str) -> None:
        with open(file_name, 'r+') as rf:
            with open(new_file_name, 'w+') as wf:
                for row in rf:
                    if '"None"' not in row:
                        wf.write(row)
                        
                        
    @classmethod
    def create_assotiation_vinyl_artist(cls, vinyl_file : str, artist_file : str, new_file : str):
        vinyl_column_info = {
            'id' : int, 
            'quantity' : int,
            'release_date' : timetype,
            'title' : str,
            'UPC' : int,
            'image_url' : str,
            'price' : float,
            'artist' : str
            
        }
        
        storage = TableInit.parse_data(vinyl_file, vinyl_column_info)
        arist_storage = TableInit.parse_data(artist_file, {'id' : int, 'name' : str})
        artists : dict[str, int] = {artist['name'] : artist['id'] for artist in arist_storage}
        with open(new_file, 'w+') as wf:
            for vinyl in storage:
                list_artist = vinyl['artist'].split(' & ')
                for v_artist in list_artist:
                    wf.write(f'{artists[v_artist]},{vinyl["id"]}\n')

    
    @classmethod
    def get_all_artist(cls, file_name : str, new_file_name : str):
        vinyl_column_info = {
            'id' : int, 
            'quantity' : int,
            'release_date' : timetype,
            'title' : str,
            'UPC' : int,
            'image_url' : str,
            'price' : float,
            'artist' : str
            
        }
        
        storage = TableInit.parse_data(file_name, vinyl_column_info)
        artist : dict[str, list] = {}
        for vinyl in storage:
            list_artist = vinyl['artist'].split(' & ')
            for i in list_artist:
                if artist.get(i) is None:
                    artist[i] = []
                artist[i].append(vinyl)
            
        with open(new_file_name, 'w+') as wf:
            for id, name in enumerate(artist.keys(), start = 1):
                wf.write(f'{id},"{name}"\n')
                
                
    @classmethod
    def sellers_vinyl_record(cls, vinyl_file : str, sellers_file : str, new_file : str):
        vinyl_ids = cls.get_ids(vinyl_file)
        sellers_ids = cls.get_ids(sellers_file)
        with open(new_file, 'w+') as wf:
            for id in vinyl_ids:
                wf.write(f'{id},{random.choice(sellers_ids)}\n')
            
            
    @classmethod
    def delete_repeat_rows_vinyl(cls, vinyl_file : str, new_file : str):
        vinyl_column_info = {
            'id' : int, 
            'quantity' : int,
            'release_date' : timetype,
            'title' : str,
            'UPC' : int,
            'image_url' : str,
            'price' : float,
            'genre' : str,
            'artist' : str
            
        }
        
        storage = TableInit.parse_data(vinyl_file, vinyl_column_info)
        names : dict = {}
        counrer = 1
        with open(new_file, 'w+') as wf:
            for vinyl in storage:
                if names.get(vinyl['title']) is None:
                    names[vinyl['title']] = vinyl
                    date : datetime.datetime = vinyl['release_date']
                    date = date.strftime('%m/%d/%Y')
                    wf.write(f'{counrer},{vinyl["quantity"]},{date},"{vinyl["title"]}",{vinyl["UPC"]},"{vinyl["image_url"]}",{vinyl["price"]},"{vinyl["artist"]}"\n')
                    counrer+=1
        
    
    @classmethod
    def create_assotiation_vinyl_record_genres(cls, vinyl_file : str, genre_file : str, new_file : str):
        vinyl_column_info = {
            'id' : int, 
            'quantity' : int,
            'release_date' : timetype,
            'title' : str,
            'UPC' : int,
            'image_url' : str,
            'price' : float,
            'genre' : str,
            'artist' : str
            
        }
        storage = TableInit.parse_data(vinyl_file, vinyl_column_info)
        genres_id = cls.get_ids(genre_file)
        with open(new_file, 'w+') as wf:
            for vinyl in storage:
                usered = []
                for _ in range(random.randint(1, 3)):
                    genre_id = random.choice(genres_id)
                    if genre_id not in usered:
                        wf.write(f'{vinyl["id"]},{genre_id}\n')
                    usered.append(genre_id)
            
