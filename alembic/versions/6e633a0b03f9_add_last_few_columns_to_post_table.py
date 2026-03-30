"""add last few columns to post table

Revision ID: 6e633a0b03f9
Revises: 2ad58f4552a1
Create Date: 2026-03-30 14:43:53.848335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e633a0b03f9'
down_revision: Union[str, Sequence[str], None] = '2ad58f4552a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',  sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts',sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')))
    pass

def downgrade() -> None:
    sa.drop_column('posts', 'published')
    sa.drop_column('posts', 'created_at')
    pass
