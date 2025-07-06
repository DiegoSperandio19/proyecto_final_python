"""create_restaurant_table

Revision ID: 1527c458b631
Revises: d52ddd047f39
Create Date: 2025-07-06 17:10:58.699103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '1527c458b631'
down_revision: Union[str, None] = 'd52ddd047f39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'restaurant',
        sa.Column('id_restaurant', sa.Uuid(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('opening_time', sa.Time(), nullable=False),
        sa.Column('closing_time', sa.Time(), nullable=False),
        sa.Column('is_eliminated', sa.Boolean(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('restaurant')
