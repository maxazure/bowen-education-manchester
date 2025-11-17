"""add_static_generation_tables

Revision ID: 589702c62e1e
Revises: 86c0c7875540
Create Date: 2025-11-18 07:54:50.292372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '589702c62e1e'
down_revision: Union[str, None] = '86c0c7875540'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建静态生成日志表
    op.create_table(
        'static_generation_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('generation_type', sa.String(length=20), nullable=False),
        sa.Column('total_pages', sa.Integer(), nullable=True, default=0),
        sa.Column('successful_pages', sa.Integer(), nullable=True, default=0),
        sa.Column('failed_pages', sa.Integer(), nullable=True, default=0),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True, default='running'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 创建静态生成详情表
    op.create_table(
        'static_generation_detail',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('log_id', sa.Integer(), nullable=False),
        sa.Column('page_type', sa.String(length=20), nullable=False),
        sa.Column('page_id', sa.Integer(), nullable=True),
        sa.Column('language', sa.String(length=5), nullable=False),
        sa.Column('url_path', sa.String(length=500), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True, default='success'),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('generation_time', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['log_id'], ['static_generation_log.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    # 删除表（按相反顺序，先删除有外键的表）
    op.drop_table('static_generation_detail')
    op.drop_table('static_generation_log')
