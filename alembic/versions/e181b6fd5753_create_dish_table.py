"""create_dish_table

Revision ID: e181b6fd5753
Revises: 1527c458b631
Create Date: 2025-07-06 17:40:48.931102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e181b6fd5753'
down_revision: Union[str, None] = '1527c458b631'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('dish',
        sa.Column('id', sa.Uuid(), nullable=False, primary_key=True),
        sa.Column('name',sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('isAvailable', sa.Boolean(), nullable=False, default=True),
        sa.Column('restaurant_id', sa.Uuid(), nullable=False),
        sa.Column('isEliminated', sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.id_restaurant'],name="FK:dish_restaurant")
    )


def downgrade() -> None:
    op.drop_table('user')
