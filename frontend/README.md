 # индификаторы - id у фильмов и узера изменить на уникальные UUid
 # tokens_schemas userout - убрать к хуям
 # ссылку редирект надо в конфигах прописать ---- user_account
 
 
 python3 -m venv env

 source env/bin/activate

 source env/bin/activate

 create file named .env and write in it :

'''

 DB_HOST = ""

 DB_PORT = ""

 DB_NAME = ""

 DB_USER = ""

 DB_PASSWORD = ""

 SECRET = "" -- any string

 ALGORITHM = "HS256"

 ACCESS_TOKEN_TTL = "P{days}DT{hours}H{minutes}M{sec}S"

 REFRESH_TOKEN_TTL = "P{days}DT{hours}H{minutes}M{sec}S" -- REFRESH_TOKEN_TTL greater than ACCESS_TOKEN_TTL

 '''



 pip install -r requirements.txt

 https://firstvds.ru/technology/ustanovka-postgresql-na-ubuntu

 alembic upgrade head

uvicorn app.main:app --reload