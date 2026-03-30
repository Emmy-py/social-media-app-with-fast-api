"""add content column to posts table

Revision ID: 1c12d55ddecf
Revises: 3dd7adf1523e
Create Date: 2026-03-30 13:22:24.775438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c12d55ddecf'
down_revision: Union[str, Sequence[str], None] = '3dd7adf1523e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False ))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
