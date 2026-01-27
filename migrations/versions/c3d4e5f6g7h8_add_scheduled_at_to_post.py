"""Add scheduled_at to post table

Revision ID: c3d4e5f6g7h8
Revises: b2c3d4e5f6g7
Create Date: 2026-01-08 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'c3d4e5f6g7h8'
down_revision = 'b2c3d4e5f6g7'
branch_labels = None
depends_on = None


def upgrade():
    # 添加 scheduled_at 列
    op.add_column('post', sa.Column('scheduled_at', sa.DateTime(), nullable=True, comment='定时发布时间'))


def downgrade():
    op.drop_column('post', 'scheduled_at')
