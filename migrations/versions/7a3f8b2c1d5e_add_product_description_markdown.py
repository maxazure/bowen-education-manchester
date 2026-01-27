"""add product description markdown fields

Revision ID: 7a3f8b2c1d5e
Revises: 1965fa370039
Create Date: 2025-01-06 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a3f8b2c1d5e'
down_revision: Union[str, None] = '1965fa370039'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add description_markdown column to product table
    op.add_column('product', sa.Column('description_markdown', sa.Text(), nullable=True, comment='详细说明Markdown源'))

    # Add description_markdown_en column to product table
    op.add_column('product', sa.Column('description_markdown_en', sa.Text(), nullable=True, comment='英文详细说明Markdown源'))


def downgrade() -> None:
    # Remove description_markdown_en column
    op.drop_column('product', 'description_markdown_en')

    # Remove description_markdown column
    op.drop_column('product', 'description_markdown')
