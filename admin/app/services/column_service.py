"""
栏目管理业务逻辑

提供栏目的树形结构构建、slug 生成等业务功能
"""

import re
from typing import List, Optional

from pypinyin import lazy_pinyin
from sqlalchemy.orm import Session

from app.models.site import SiteColumn


def build_tree(db: Session, parent_id: Optional[int] = None) -> List[SiteColumn]:
    """
    构建栏目树形结构

    Args:
        db: 数据库会话
        parent_id: 父栏目 ID（None 表示顶级栏目）

    Returns:
        树形结构的栏目列表（每个栏目包含 children 属性）
    """
    # 查询指定父级下的所有栏目
    columns = (
        db.query(SiteColumn)
        .filter_by(parent_id=parent_id)
        .order_by(SiteColumn.sort_order, SiteColumn.id)
        .all()
    )

    # 递归构建树
    tree = []
    for column in columns:
        # 获取子栏目
        column.children = build_tree(db, column.id)
        # 添加层级属性（用于前端显示缩进）
        column.level = 0 if parent_id is None else _get_column_level(db, column.id)
        tree.append(column)

    return tree


def get_all_columns(db: Session, enabled_only: bool = False) -> List[SiteColumn]:
    """
    获取所有栏目（扁平列表）

    Args:
        db: 数据库会话
        enabled_only: 是否只返回已启用的栏目

    Returns:
        栏目列表
    """
    query = db.query(SiteColumn).order_by(SiteColumn.sort_order, SiteColumn.id)

    if enabled_only:
        query = query.filter_by(is_enabled=True)

    return query.all()


def get_column_by_id(db: Session, column_id: int) -> Optional[SiteColumn]:
    """
    根据 ID 获取栏目

    Args:
        db: 数据库会话
        column_id: 栏目 ID

    Returns:
        栏目对象，不存在返回 None
    """
    return db.query(SiteColumn).filter_by(id=column_id).first()


def get_column_by_slug(db: Session, slug: str) -> Optional[SiteColumn]:
    """
    根据 slug 获取栏目

    Args:
        db: 数据库会话
        slug: URL slug

    Returns:
        栏目对象，不存在返回 None
    """
    return db.query(SiteColumn).filter_by(slug=slug).first()


def generate_slug(name: str, db: Session) -> str:
    """
    自动生成 URL slug

    从栏目名称生成 slug，如果重复则添加数字后缀

    Args:
        name: 栏目名称
        db: 数据库会话

    Returns:
        唯一的 URL slug
    """
    # 中文转拼音
    pinyin_list = lazy_pinyin(name)
    base_slug = "-".join(pinyin_list).lower()

    # 清理非法字符
    base_slug = re.sub(r"[^\w\-]", "", base_slug)
    base_slug = re.sub(r"\-+", "-", base_slug)
    base_slug = base_slug.strip("-")

    # 如果为空，使用默认值
    if not base_slug:
        base_slug = "column"

    # 检查是否重复
    slug = base_slug
    counter = 1
    while get_column_by_slug(db, slug) is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


def can_delete_column(db: Session, column_id: int) -> bool:
    """
    检查栏目是否可以删除

    如果栏目有子栏目或关联内容，则不允许删除

    Args:
        db: 数据库会话
        column_id: 栏目 ID

    Returns:
        是否可以删除
    """
    column = get_column_by_id(db, column_id)
    if not column:
        return False

    # 检查是否有子栏目
    children_count = db.query(SiteColumn).filter_by(parent_id=column_id).count()
    if children_count > 0:
        return False

    # TODO: 检查是否有关联的文章、产品等内容
    # 这里需要根据实际的数据模型进行检查

    return True


def get_statistics(db: Session) -> dict:
    """
    获取栏目统计信息

    Returns:
        统计数据字典
    """
    total = db.query(SiteColumn).count()
    enabled = db.query(SiteColumn).filter_by(is_enabled=True).count()
    disabled = total - enabled
    top_level = db.query(SiteColumn).filter_by(parent_id=None).count()

    return {
        "total": total,
        "enabled": enabled,
        "disabled": disabled,
        "top_level": top_level,
    }


def _get_column_level(db: Session, column_id: int) -> int:
    """
    获取栏目的层级深度

    Args:
        db: 数据库会话
        column_id: 栏目 ID

    Returns:
        层级深度（0 表示顶级）
    """
    column = get_column_by_id(db, column_id)
    if not column or column.parent_id is None:
        return 0

    return 1 + _get_column_level(db, column.parent_id)
