"""add_hero_tagline_en_to_site_column

Revision ID: b4e99ed474b9
Revises: 589702c62e1e
Create Date: 2025-11-18 10:47:03.173455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4e99ed474b9'
down_revision: Union[str, None] = '589702c62e1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add hero_tagline_en column to site_column table
    op.add_column('site_column', sa.Column('hero_tagline_en', sa.Text(), nullable=True, comment='Hero英文标语/口号'))


def downgrade() -> None:
    # Remove hero_tagline_en column from site_column table
    op.drop_column('site_column', 'hero_tagline_en')
