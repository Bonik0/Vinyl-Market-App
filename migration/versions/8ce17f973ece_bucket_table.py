"""bucket_table

Revision ID: 8ce17f973ece
Revises: f419a1b7c890
Create Date: 2024-12-16 22:18:58.214875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from migration.TableInit import TableInit

# revision identifiers, used by Alembic.
revision: str = '8ce17f973ece'
down_revision: Union[str, None] = 'f419a1b7c890'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE bucket (
            user_id INTEGER,
            vinyl_record_id INTEGER,
            created_at TIMESTAMP DEFAULT current_timestamp,
            PRIMARY KEY (user_id, vinyl_record_id),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (vinyl_record_id) REFERENCES vinyl_records (id) ON DELETE CASCADE
        );  
        """
    )
    op.execute("""
                CREATE VIEW bucket_ids AS
                SELECT vinyl_record_id, user_id
                FROM bucket
                ORDER BY created_at DESC, vinyl_record_id DESC;
               """
            )
    bucket_column_types = {
        'user_id' : int,
        'vinyl_record_id' : int
    }
    bucket = TableInit.parse_data('./migration/versions/csv_data/bucket.csv', bucket_column_types)
    for item in bucket:
        op.execute(
            sa.text("INSERT INTO bucket (user_id, vinyl_record_id) VALUES (:user_id, :vinyl_record_id)").params(item)
        )

def downgrade() -> None:
    op.execute(
        """
        DROP VIEW bucket_ids;
        """
    )
    op.execute(
        """
        DROP TABLE bucket;
        """
    )
