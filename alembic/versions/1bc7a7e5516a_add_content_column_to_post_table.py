"""add content column to post table

Revision ID: 1bc7a7e5516a
Revises: 64f36aa6fb54
Create Date: 2023-11-11 22:57:53.297716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bc7a7e5516a'
down_revision: Union[str, None] = '64f36aa6fb54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
