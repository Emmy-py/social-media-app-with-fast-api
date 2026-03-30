"""create posts table

Revision ID: 3dd7adf1523e
Revises: 5a4b5907f2f2
Create Date: 2026-03-30 12:18:10.505076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dd7adf1523e'
down_revision: Union[str, Sequence[str], None] = '5a4b5907f2f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
