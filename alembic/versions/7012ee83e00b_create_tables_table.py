"""create_tables_table

Revision ID: 7012ee83e00b
Revises: 1527c458b631
Create Date: 2025-07-06 23:42:34.452253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7012ee83e00b'
down_revision: Union[str, None] = '1527c458b631'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('tables',
        sa.Column('id_table', sa.Uuid(), nullable=False, primary_key=True),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('is_eliminated', sa.Boolean(), nullable=False),
        sa.Column('id_restaurant', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['id_restaurant'], ['restaurant.id_restaurant'],name="FK:restaurants")
    )


def downgrade() -> None:
    op.drop_table('tables')
