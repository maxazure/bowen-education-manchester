"""Create content_version table

Revision ID: a1b2c3d4e5f6
Revises: 38e876557ca4
Create Date: 2026-01-08 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'a1b2c3d4e5f6'
down_revision = '38e876557ca4'
branch_labels = None
depends_on = None


def upgrade():
    # 创建 content_version 表
    op.create_table(
        'content_version',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('content_type', sa.String(20), nullable=False),
        sa.Column('content_id', sa.Integer(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False, default=1),
        sa.Column('title', sa.String(200), nullable=True),
        sa.Column('content_snapshot', sa.Text(), nullable=True),
        sa.Column('action', sa.String(20), nullable=False),
        sa.Column('admin_id', sa.Integer(), nullable=True),
        sa.Column('admin_name', sa.String(100), nullable=True),
        sa.Column('remark', sa.String(500), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 添加索引
    op.create_index('idx_content_version_type_id', 'content_version', ['content_type', 'content_id'])
    op.create_index('idx_content_version_created', 'content_version', ['created_at'])


def downgrade():
    op.drop_index('idx_content_version_created', table_name='content_version')
    op.drop_index('idx_content_version_type_id', table_name='content_version')
    op.drop_table('content_version')
