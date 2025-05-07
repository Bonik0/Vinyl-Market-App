"""assotiation_vinyl_table

Revision ID: f419a1b7c890
Revises: ba7d5cecd760
Create Date: 2024-12-15 19:02:48.771695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from migration.TableInit import TableInit

# revision identifiers, used by Alembic.
revision: str = 'f419a1b7c890'
down_revision: Union[str, None] = 'ba7d5cecd760'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE genre_assotiation (
            genre_id INTEGER,
            vinyl_record_id INTEGER,
            PRIMARY KEY (genre_id, vinyl_record_id),
            FOREIGN KEY (genre_id) REFERENCES genres (id) ON DELETE CASCADE,
            FOREIGN KEY (vinyl_record_id) REFERENCES vinyl_records (id) ON DELETE CASCADE
        );  
        """
    )
    op.execute(
        """
        CREATE TABLE artist_assotiation (
            artist_id INTEGER,
            vinyl_record_id INTEGER,
            PRIMARY KEY (artist_id, vinyl_record_id),
            FOREIGN KEY (artist_id) REFERENCES artists (id) ON DELETE CASCADE,
            FOREIGN KEY (vinyl_record_id) REFERENCES vinyl_records (id) ON DELETE CASCADE
        );  
        """
    )
    vinyl_genres_columns_types = {
        'vinyl_record_id' : int,
        'genre_id' : int
    }
    vinyl_genres = TableInit.parse_data('./migration/versions/csv_data/assotiation_vinyl_title_genre.csv', vinyl_genres_columns_types)
    for assotiation in vinyl_genres:
        op.execute(
            sa.text("INSERT INTO genre_assotiation (vinyl_record_id, genre_id) VALUES (:vinyl_record_id, :genre_id)").params(assotiation)
        )
    vinyl_artist_columns_types = {
        'artist_id' : int,
        'vinyl_record_id' : int
    }
    vinyl_artist = TableInit.parse_data('./migration/versions/csv_data/assotiation_vinyl_artist.csv', vinyl_artist_columns_types)
    for assotiation in vinyl_artist:
        op.execute(
            sa.text("INSERT INTO artist_assotiation (vinyl_record_id, artist_id) VALUES (:vinyl_record_id, :artist_id)").params(assotiation)
        )
        
    


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE genre_assotiation;
        """
    )
    op.execute(
        """
        DROP TABLE artist_assotiation;
        """
    )
