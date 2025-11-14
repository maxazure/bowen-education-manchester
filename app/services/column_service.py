"""
栏目服务层

提供栏目相关的业务逻辑功能：
- Slug 自动生成和唯一性验证
- 栏目删除前的关联检查
- 树形结构构建
- 导航和底部栏目获取
- 面包屑导航生成
"""

from typing import Dict, List, Optional

from slugify import slugify
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.product import Product
from app.models.site import SiteColumn, SinglePage, ColumnType
from app.models.gallery import Gallery


def generate_slug(name: str, db: Session, exclude_id: Optional[int] = None) -> str:
    """
    生成唯一的 URL Slug

    Args:
        name: 栏目名称
        db: 数据库会话
        exclude_id: 排除的栏目 ID（用于更新时）

    Returns:
        唯一的 slug 字符串

    Examples:
        >>> generate_slug("关于我们", db)
        'guan-yu-wo-men'
        >>> generate_slug("About Us", db)
        'about-us'
    """
    base_slug = slugify(name)

    # 检查 slug 是否已存在
    query = db.query(SiteColumn).filter(SiteColumn.slug == base_slug)
    if exclude_id:
        query = query.filter(SiteColumn.id != exclude_id)

    existing = query.first()
    if not existing:
        return base_slug

    # 如果存在重复，添加数字后缀
    counter = 1
    while True:
        new_slug = f"{base_slug}-{counter}"
        query = db.query(SiteColumn).filter(SiteColumn.slug == new_slug)
        if exclude_id:
            query = query.filter(SiteColumn.id != exclude_id)

        if not query.first():
            return new_slug
        counter += 1


def can_delete_column(db: Session, column_id: int) -> bool:
    """
    检查栏目是否可以删除

    如果栏目下有关联内容（文章、产品等），则不能删除

    Args:
        db: 数据库会话
        column_id: 栏目 ID

    Returns:
        True 可以删除，False 不能删除
    """
    # 检查是否有文章关联
    post_count = db.query(Post).filter(Post.column_id == column_id).count()
    if post_count > 0:
        return False

    # 检查是否有产品关联
    product_count = db.query(Product).filter(Product.column_id == column_id).count()
    if product_count > 0:
        return False

    # 检查是否有子栏目
    child_count = db.query(SiteColumn).filter(SiteColumn.parent_id == column_id).count()
    if child_count > 0:
        return False

    return True


def build_tree(db: Session, parent_id: Optional[int] = None) -> List[SiteColumn]:
    """
    构建栏目树形结构

    Args:
        db: 数据库会话
        parent_id: 父栏目 ID（None 表示获取顶级栏目）

    Returns:
        树形结构的栏目列表（模型对象，包含 children, level, content_id 属性）
    """
    # 获取指定父级的所有子栏目
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.parent_id == parent_id)
        .order_by(SiteColumn.sort_order, SiteColumn.id)
        .all()
    )

    result = []
    for column in columns:
        # 递归构建子树
        column.children = build_tree(db, column.id)

        # 添加层级属性
        column.level = _get_column_level(db, column.id)

        # 添加关联内容ID
        column.content_id = _get_content_id(db, column)

        result.append(column)

    return result


def _get_column_level(db: Session, column_id: int) -> int:
    """
    获取栏目的层级深度

    Args:
        db: 数据库会话
        column_id: 栏目 ID

    Returns:
        层级深度（0 表示顶级）
    """
    column = db.query(SiteColumn).filter_by(id=column_id).first()
    if not column or column.parent_id is None:
        return 0

    return 1 + _get_column_level(db, column.parent_id)


def _get_content_id(db: Session, column: SiteColumn) -> Optional[int]:
    """
    根据栏目类型获取关联内容的ID

    Args:
        db: 数据库会话
        column: 栏目对象

    Returns:
        关联内容的ID，如果没有则返回 None
    """
    # 单页面类型 - 查询 single_page 表
    if column.column_type == ColumnType.SINGLE_PAGE:
        page = db.query(SinglePage).filter_by(column_id=column.id).first()
        return page.id if page else None

    # 其他类型没有关联内容ID
    return None


def get_nav_columns(db: Session) -> List[SiteColumn]:
    """
    获取导航显示的栏目

    返回启用且设置为显示在导航的栏目，按排序值排序

    Args:
        db: 数据库会话

    Returns:
        导航栏目列表
    """
    return (
        db.query(SiteColumn)
        .filter(SiteColumn.show_in_nav == True, SiteColumn.is_enabled == True)
        .order_by(SiteColumn.sort_order, SiteColumn.id)
        .all()
    )


def get_footer_columns(db: Session) -> List[SiteColumn]:
    """
    获取底部显示的栏目

    返回启用且设置为显示在底部的栏目（menu_location 为 "footer" 或 "both"）

    Args:
        db: 数据库会话

    Returns:
        底部栏目列表
    """
    return (
        db.query(SiteColumn)
        .filter(
            SiteColumn.is_enabled == True,
            or_(
                SiteColumn.menu_location == "footer", SiteColumn.menu_location == "both"
            ),
        )
        .order_by(SiteColumn.sort_order, SiteColumn.id)
        .all()
    )


def get_breadcrumbs(db: Session, column_id: int) -> List[Dict]:
    """
    获取面包屑导航

    从当前栏目向上追溯到顶级栏目

    Args:
        db: 数据库会话
        column_id: 当前栏目 ID

    Returns:
        面包屑列表（从顶级到当前）

    Examples:
        [
            {"id": 1, "name": "首页", "slug": "home"},
            {"id": 2, "name": "关于我们", "slug": "about"},
            {"id": 3, "name": "团队介绍", "slug": "team"}
        ]
    """
    breadcrumbs = []
    current_column = db.query(SiteColumn).filter_by(id=column_id).first()

    # 向上追溯父栏目
    while current_column:
        breadcrumbs.insert(
            0,
            {
                "id": current_column.id,
                "name": current_column.name,
                "slug": current_column.slug,
            },
        )
        if current_column.parent_id:
            current_column = (
                db.query(SiteColumn).filter_by(id=current_column.parent_id).first()
            )
        else:
            current_column = None

    return breadcrumbs


def get_column_by_slug(db: Session, slug: str) -> Optional[SiteColumn]:
    """
    根据 slug 获取栏目

    Args:
        db: 数据库会话
        slug: URL slug

    Returns:
        栏目对象或 None
    """
    return db.query(SiteColumn).filter_by(slug=slug).first()


def get_all_columns(db: Session, enabled_only: bool = False) -> List[SiteColumn]:
    """
    获取所有栏目

    Args:
        db: 数据库会话
        enabled_only: 是否只返回启用的栏目

    Returns:
        栏目列表
    """
    query = db.query(SiteColumn).order_by(SiteColumn.sort_order, SiteColumn.id)

    if enabled_only:
        query = query.filter(SiteColumn.is_enabled == True)

    return query.all()
