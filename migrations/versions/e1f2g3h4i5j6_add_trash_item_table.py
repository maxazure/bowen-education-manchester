"""Add trash item table for soft delete functionality

Revision ID: e1f2g3h4i5j6
Revises: 38e876557ca4
Create Date: 2026-01-08 12:00:00

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'e1f2g3h4i5j6'
down_revision = '38e876557ca4'
branch_labels = None
depends_on = None


def upgrade():
    # Create trash_item table
    op.create_table(
        'trash_item',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('content_type', sa.String(50), nullable=False, comment='内容类型'),
        sa.Column('content_id', sa.Integer(), nullable=False, comment='原始内容ID'),
        sa.Column('original_data', sa.Text(), nullable=False, comment='原始数据JSON'),
        sa.Column('deleted_at', sa.DateTime(), nullable=False, comment='删除时间'),
        sa.Column('deleted_by', sa.Integer(), nullable=True, comment='删除人ID'),
        sa.Column('delete_reason', sa.String(500), nullable=True, comment='删除原因'),
        sa.Column('storage_size', sa.Integer(), default=0, nullable=False, comment='存储大小'),
        sa.PrimaryKey('id'),
        sa.Index('idx_trash_content', 'content_type', 'content_id'),
        sa.Index('idx_trash_deleted', 'deleted_at'),
    )


def downgrade():
    op.drop_table('trash_item')
