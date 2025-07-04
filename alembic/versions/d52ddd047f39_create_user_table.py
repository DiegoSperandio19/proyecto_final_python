"""create_user_table

Revision ID: d52ddd047f39
Revises: 0ee13e753afc
Create Date: 2025-07-04 10:02:19.627130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd52ddd047f39'
down_revision: Union[str, None] = '0ee13e753afc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
        sa.Column('id', sa.Uuid(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('user')
