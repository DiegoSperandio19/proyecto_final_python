"""create_role_table

Revision ID: e6fd96c298c4
Revises: d52ddd047f39
Create Date: 2025-07-05 11:53:30.378817

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e6fd96c298c4'
down_revision: Union[str, None] = '0ee13e753afc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('role',
        sa.Column('id', sa.Uuid(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('scopes', postgresql.ARRAY(sa.String()), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('role')
