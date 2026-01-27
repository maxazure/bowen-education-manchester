"""Add operation log table

Revision ID: f2g3h4i5j6k7
Revises: e1f2g3h4i5j6
Create Date: 2026-01-08 12:30:00

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f2g3h4i5j6k7'
down_revision = 'e1f2g3h4i5j6'
branch_labels = None
depends_on = None


def upgrade():
    # Create operation_log table
    op.create_table(
        'operation_log',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('admin_user_id', sa.Integer(), nullable=True, comment='管理员ID'),
        sa.Column('admin_username', sa.String(100), nullable=True, comment='管理员用户名'),
        sa.Column('action', sa.String(50), nullable=False, comment='操作类型'),
        sa.Column('module', sa.String(50), nullable=False, comment='操作模块'),
        sa.Column('target_type', sa.String(50), nullable=True, comment='目标类型'),
        sa.Column('target_id', sa.Integer(), nullable=True, comment='目标ID'),
        sa.Column('target_name', sa.String(200), nullable=True, comment='目标名称'),
        sa.Column('description', sa.String(500), nullable=True, comment='操作描述'),
        sa.Column('old_data', sa.JSON(), nullable=True, comment='操作前数据'),
        sa.Column('new_data', sa.JSON(), nullable=True, comment='操作后数据'),
        sa.Column('ip_address', sa.String(45), nullable=True, comment='IP地址'),
        sa.Column('user_agent', sa.String(500), nullable=True, comment='User Agent'),
        sa.Column('status', sa.String(20), default='success', nullable=False, comment='状态'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='错误信息'),
        sa.PrimaryKey('id'),
        sa.Index('idx_op_log_admin', 'admin_user_id'),
        sa.Index('idx_op_log_action', 'action'),
        sa.Index('idx_op_log_module', 'module'),
        sa.Index('idx_op_log_created', 'created_at'),
    )


def downgrade():
    op.drop_table('operation_log')
