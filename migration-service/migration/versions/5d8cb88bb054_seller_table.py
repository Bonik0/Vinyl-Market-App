"""seller_table

Revision ID: 5d8cb88bb054
Revises: 91b8485375a3
Create Date: 2024-12-15 14:00:29.740048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from migration.TableInit import TableInit

# revision identifiers, used by Alembic.
revision: str = '5d8cb88bb054'
down_revision: Union[str, None] = '91b8485375a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE sellers (
            user_id INTEGER NOT NULL,
            phone_number VARCHAR(15) NOT NULL,
            city VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL,
            PRIMARY KEY (user_id),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );  
        """
    )
    op.execute(
        """
        CREATE FUNCTION update_new_sellers_role()
        RETURNS TRIGGER AS $sellers_change_role$
            BEGIN
                UPDATE users
                SET role = 'seller'
                WHERE id = NEW.user_id;

                RETURN NEW;
            END;
        $sellers_change_role$ language plpgsql;
        """
    )
    
    op.execute(
        """ CREATE TRIGGER sellers_change_role
            BEFORE INSERT ON sellers
            FOR EACH ROW 
            EXECUTE FUNCTION update_new_sellers_role();
        """
    )
    sellers_columns_types = {
        'user_id' : int,
        'phone_number' : str, 
        'city' : str,
        'country' : str
    }
    sellers = TableInit.parse_data('./migration/versions/csv_data/seller.csv', sellers_columns_types)
    for seller in sellers:
        print(seller)
        op.execute(
            sa.text("INSERT INTO sellers (user_id, phone_number, city, country) VALUES (:user_id, :phone_number, :city, :country)").params(seller)
        )
    


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER sellers_change_role ON sellers;
        """
    )
    op.execute(
        """
        DROP FUNCTION update_new_sellers_role();
        """
    )
    op.execute(
        """
        DROP TABLE sellers;
        """
    )
