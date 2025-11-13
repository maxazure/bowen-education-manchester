"""add content_markdown and is_pinned to post

Revision ID: 86c0c7875540
Revises: 3c60c9ca6db1
Create Date: 2025-11-13 15:39:40.346906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86c0c7875540'
down_revision: Union[str, None] = '3c60c9ca6db1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add content_markdown column to post table
    op.add_column('post', sa.Column('content_markdown', sa.Text(), nullable=True, comment='Markdown原文'))

    # Add is_pinned column to post table
    op.add_column('post', sa.Column('is_pinned', sa.Boolean(), nullable=False, server_default='0', comment='是否置顶'))


def downgrade() -> None:
    # Remove is_pinned column
    op.drop_column('post', 'is_pinned')

    # Remove content_markdown column
    op.drop_column('post', 'content_markdown')
