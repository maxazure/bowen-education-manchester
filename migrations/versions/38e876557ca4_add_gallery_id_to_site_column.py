"""add_gallery_id_to_site_column

Revision ID: 38e876557ca4
Revises: b4e99ed474b9
Create Date: 2025-11-18 22:46:55.427731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38e876557ca4'
down_revision: Union[str, None] = 'b4e99ed474b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 添加 gallery_id 列到 site_column 表
    op.add_column('site_column', sa.Column('gallery_id', sa.Integer(), nullable=True, comment='关联的Gallery ID'))

    # 创建外键约束（SQLite需要特殊处理）
    with op.batch_alter_table('site_column', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_site_column_gallery_id', 'gallery', ['gallery_id'], ['id'])


def downgrade() -> None:
    # 删除外键约束和列
    with op.batch_alter_table('site_column', schema=None) as batch_op:
        batch_op.drop_constraint('fk_site_column_gallery_id', type_='foreignkey')
        batch_op.drop_column('gallery_id')
