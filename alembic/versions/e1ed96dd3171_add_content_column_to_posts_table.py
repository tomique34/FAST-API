"""add content column to posts table

Revision ID: e1ed96dd3171
Revises: 207e059ef3e8
Create Date: 2024-09-17 15:08:12.668228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1ed96dd3171'
down_revision: Union[str, None] = '207e059ef3e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
