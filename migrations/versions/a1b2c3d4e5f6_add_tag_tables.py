"""Add tag tables for content tagging system

Revision ID: a1b2c3d4e5f6
Revises: 38e876557ca4
Create Date: 2026-01-08

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic
revision = 'a1b2c3d4e5f6'
down_revision = '38e876557ca4'
branch_labels = None
depends_on = None


def upgrade():
    # Create tag table
    op.create_table(
        'tag',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False, comment='标签名称'),
        sa.Column('name_en', sa.String(100), nullable=True, comment='标签英文名称'),
        sa.Column('slug', sa.String(50), nullable=False, unique=True, comment='标签Slug'),
        sa.Column('color', sa.String(7), nullable=False, default='#667eea', comment='标签颜色'),
        sa.Column('description', sa.Text(), nullable=True, comment='标签描述'),
        sa.Column('description_en', sa.Text(), nullable=True, comment='标签英文描述'),
        sa.Column('icon', sa.String(50), nullable=True, comment='标签图标'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='是否启用'),
        sa.Column('sort_order', sa.Integer(), nullable=False, default=0, comment='排序序号'),
        sa.PrimaryKey('id'),
    )

    # Create post_tag_link table
    op.create_table(
        'post_tag_link',
        sa.Column('post_id', sa.Integer(), nullable=False, comment='文章ID'),
        sa.Column('tag_id', sa.Integer(), nullable=False, comment='标签ID'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='关联创建时间'),
        sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
        sa.PrimaryKeyConstraint('post_id', 'tag_id')
    )

    # Create index for faster lookups
    op.create_index('ix_tag_slug', 'tag', ['slug'], unique=True)
    op.create_index('ix_tag_is_active', 'tag', ['is_active'])
    op.create_index('ix_post_tag_link_post_id', 'post_tag_link', ['post_id'])
    op.create_index('ix_post_tag_link_tag_id', 'post_tag_link', ['tag_id'])


def downgrade():
    op.drop_index('ix_post_tag_link_tag_id', table_name='post_tag_link')
    op.drop_index('ix_post_tag_link_post_id', table_name='post_tag_link')
    op.drop_index('ix_tag_is_active', table_name='tag')
    op.drop_index('ix_tag_slug', table_name='tag')
    op.drop_table('post_tag_link')
    op.drop_table('tag')
