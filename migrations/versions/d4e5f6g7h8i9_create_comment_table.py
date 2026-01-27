"""Create comment table

Revision ID: d4e5f6g7h8i9
Revises: c3d4e5f6g7h8
Create Date: 2026-01-08 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'd4e5f6g7h8i9'
down_revision = 'c3d4e5f6g7h8'
branch_labels = None
depends_on = None


def upgrade():
    # 创建 comment 表
    op.create_table(
        'comment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('content_type', sa.String(20), nullable=False),
        sa.Column('content_id', sa.Integer(), nullable=False),
        sa.Column('author_name', sa.String(100), nullable=False),
        sa.Column('author_email', sa.String(200), nullable=True),
        sa.Column('author_ip', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, default='pending'),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('reviewed_by', sa.Integer(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(), nullable=True),
        sa.Column('reply_content', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 添加索引
    op.create_index('idx_comment_content', 'comment', ['content_type', 'content_id'])
    op.create_index('idx_comment_status', 'comment', ['status'])
    op.create_index('idx_comment_created', 'comment', ['created_at'])


def downgrade():
    op.drop_index('idx_comment_created', table_name='comment')
    op.drop_index('idx_comment_status', table_name='comment')
    op.drop_index('idx_comment_content', table_name='comment')
    op.drop_table('comment')
