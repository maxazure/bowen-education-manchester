"""add_hero_slides_table

Revision ID: 1965fa370039
Revises: 38e876557ca4
Create Date: 2025-11-19 10:44:51.890357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1965fa370039'
down_revision: Union[str, None] = '38e876557ca4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建 hero_slides 表
    op.create_table(
        'hero_slides',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False, comment='标题'),
        sa.Column('title_en', sa.String(length=200), nullable=True, comment='英文标题'),
        sa.Column('subtitle', sa.String(length=300), nullable=True, comment='副标题'),
        sa.Column('subtitle_en', sa.String(length=300), nullable=True, comment='英文副标题'),
        sa.Column('description', sa.Text(), nullable=True, comment='描述'),
        sa.Column('description_en', sa.Text(), nullable=True, comment='英文描述'),
        sa.Column('background_image', sa.String(length=500), nullable=False, comment='背景图片路径'),
        sa.Column('badge_text', sa.String(length=100), nullable=True, comment='徽章文字'),
        sa.Column('badge_text_en', sa.String(length=100), nullable=True, comment='英文徽章文字'),
        sa.Column('button_text', sa.String(length=100), nullable=True, comment='按钮文字'),
        sa.Column('button_text_en', sa.String(length=100), nullable=True, comment='英文按钮文字'),
        sa.Column('button_url', sa.String(length=500), nullable=True, comment='按钮链接'),
        sa.Column('button_style', sa.String(length=50), nullable=True, comment='按钮样式'),
        sa.Column('button2_text', sa.String(length=100), nullable=True, comment='第二个按钮文字'),
        sa.Column('button2_text_en', sa.String(length=100), nullable=True, comment='第二个按钮英文文字'),
        sa.Column('button2_url', sa.String(length=500), nullable=True, comment='第二个按钮链接'),
        sa.Column('button2_style', sa.String(length=50), nullable=True, comment='第二个按钮样式'),
        sa.Column('sort_order', sa.Integer(), nullable=True, comment='排序顺序（数字越小越靠前）'),
        sa.Column('is_active', sa.Boolean(), nullable=True, comment='是否启用'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # 删除 hero_slides 表
    op.drop_table('hero_slides')
