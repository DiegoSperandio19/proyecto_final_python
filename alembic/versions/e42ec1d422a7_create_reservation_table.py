"""create_reservation_table

Revision ID: e42ec1d422a7
Revises: e181b6fd5753
Create Date: 2025-07-07 12:06:14.623721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e42ec1d422a7'
down_revision: Union[str, None] = 'e181b6fd5753'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('reservation',
        sa.Column('id', sa.Uuid(), nullable=False, primary_key=True),
        sa.Column('id_user', sa.Uuid(), nullable=True),
        sa.Column('id_table', sa.Uuid(), nullable=True),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('reservation_date', sa.Date(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, default='Pending'),
        sa.Column('is_eliminated', sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(['id_user'], ['user.id'], name="FK:reservation_user"),
        sa.ForeignKeyConstraint(['id_table'], ['tables.id_table'], name="FK:reservation_table")
    )


def downgrade() -> None:
    op.drop_table('reservation')
