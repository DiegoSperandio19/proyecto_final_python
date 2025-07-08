"""create_preorder_table

Revision ID: 268edf30e6bf
Revises: e42ec1d422a7
Create Date: 2025-07-07 20:20:07.437895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '268edf30e6bf'
down_revision: Union[str, None] = 'e42ec1d422a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('preorder',
        sa.Column('id', sa.Uuid(), nullable=False, primary_key=True),
        sa.Column('id_reservation', sa.Uuid(), nullable=True),
        sa.Column('id_user', sa.Uuid(), nullable=True),
        sa.Column('id_table', sa.Uuid(), nullable=True),
        sa.Column('id_dish', sa.Uuid(), nullable=True),
        sa.Column('n_dishes', sa.Integer(), nullable=False),
        sa.Column('is_eliminated', sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(['id_reservation'], ['reservation.id'], name="FK:preorder_reservation"),
        sa.ForeignKeyConstraint(['id_user'], ['user.id'], name="FK:preorder_user"),
        sa.ForeignKeyConstraint(['id_table'], ['tables.id_table'], name="FK:preorder_table"),
        sa.ForeignKeyConstraint(['id_dish'], ['dish.id'], name="FK:preorder_dish")
    )

def downgrade() -> None:
    op.drop_table('preorder')
