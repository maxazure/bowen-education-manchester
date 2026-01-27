"""Create notification table

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2026-01-08 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'b2c3d4e5f6g7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # 创建 notification 表
    op.create_table(
        'notification',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('type', sa.String(20), nullable=False, default='system'),
        sa.Column('level', sa.String(20), nullable=False, default='info'),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('link', sa.String(500), nullable=True),
        sa.Column('link_text', sa.String(100), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False, default=False),
        sa.Column('read_at', sa.DateTime(), nullable=True),
        sa.Column('recipient_id', sa.Integer(), nullable=True),
        sa.Column('recipient_role', sa.String(50), nullable=False, default='admin'),
        sa.PrimaryKeyConstraint('id')
    )

    # 添加索引
    op.create_index('idx_notification_recipient', 'notification', ['recipient_role', 'is_read'])
    op.create_index('idx_notification_created', 'notification', ['created_at'])


def downgrade():
    op.drop_index('idx_notification_created', table_name='notification')
    op.drop_index('idx_notification_recipient', table_name='notification')
    op.drop_table('notification')
