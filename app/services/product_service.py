# -*- coding: utf-8 -*-
"""Product Service - Products and categories"""

from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.models import Product, ProductCategory
from app.utils.cache import cache_content


@cache_content
def get_product_categories(
    db: Session, column_id: int, visible_only: bool = True
) -> List[ProductCategory]:
    """
    Get product categories for a column (cached for 5 minutes)

    Args:
        db: Database session
        column_id: Column ID
        visible_only: Only return visible categories

    Returns:
        List of ProductCategory objects
    """
    query = db.query(ProductCategory).filter(ProductCategory.column_id == column_id)

    if visible_only:
        query = query.filter(ProductCategory.is_visible.is_(True))

    return query.order_by(ProductCategory.sort_order).all()


@cache_content
def get_products(
    db: Session,
    column_id: Optional[int] = None,
    category_id: Optional[int] = None,
    is_recommended: Optional[bool] = None,
    status: str = "online",
    limit: Optional[int] = None,
    offset: int = 0,
) -> List[Product]:
    """
    Get products with filters (cached for 5 minutes)

    Args:
        db: Database session
        column_id: Filter by column ID
        category_id: Filter by category ID
        is_recommended: Filter by recommended status
        status: Filter by status (default: online)
        limit: Maximum number of products to return
        offset: Number of products to skip

    Returns:
        List of Product objects
    """
    query = (
        db.query(Product)
        .options(joinedload(Product.cover_media))
        .filter(Product.status == status)
    )

    if column_id:
        query = query.filter(Product.column_id == column_id)

    if category_id:
        query = query.join(Product.categories).filter(ProductCategory.id == category_id)

    if is_recommended is not None:
        query = query.filter(Product.is_recommended == is_recommended)

    query = query.order_by(Product.published_at.desc(), Product.id.desc())

    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(limit)

    return query.all()


def get_product_by_slug(
    db: Session, slug: str, status: str = "online"
) -> Optional[Product]:
    """
    Get product by slug

    Args:
        db: Database session
        slug: Product slug
        status: Filter by status

    Returns:
        Product object or None
    """
    return (
        db.query(Product)
        .options(
            joinedload(Product.cover_media),
            joinedload(Product.categories),
            joinedload(Product.custom_field_values),
        )
        .filter(Product.slug == slug, Product.status == status)
        .first()
    )


def get_product_count(
    db: Session,
    column_id: Optional[int] = None,
    category_id: Optional[int] = None,
    status: str = "online",
) -> int:
    """
    Get product count

    Args:
        db: Database session
        column_id: Filter by column ID
        category_id: Filter by category ID
        status: Filter by status

    Returns:
        Number of products
    """
    query = db.query(Product).filter(Product.status == status)

    if column_id:
        query = query.filter(Product.column_id == column_id)

    if category_id:
        query = query.join(Product.categories).filter(ProductCategory.id == category_id)

    return query.count()


# ===== 管理后台功能 =====


def generate_slug(name: str, db: Session, exclude_id: Optional[int] = None) -> str:
    """
    生成唯一的 slug

    Args:
        name: 产品名称
        db: 数据库会话
        exclude_id: 排除的产品 ID (用于更新时)

    Returns:
        唯一的 slug
    """
    from app.services.single_page_service import slugify

    base_slug = slugify(name)

    if not base_slug:
        base_slug = "product"

    # 检查 slug 是否已存在
    query = db.query(Product).filter(Product.slug == base_slug)
    if exclude_id:
        query = query.filter(Product.id != exclude_id)

    existing = query.first()

    if not existing:
        return base_slug

    # 如果已存在,添加数字后缀
    counter = 1
    while True:
        new_slug = f"{base_slug}-{counter}"
        query = db.query(Product).filter(Product.slug == new_slug)
        if exclude_id:
            query = query.filter(Product.id != exclude_id)

        if not query.first():
            return new_slug

        counter += 1


def can_delete_product(db: Session, product_id: int) -> tuple[bool, str]:
    """
    检查产品是否可以删除

    Args:
        db: 数据库会话
        product_id: 产品 ID

    Returns:
        (是否可以删除, 错误消息)
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return False, "产品不存在"

    # 产品可以直接删除,无需特殊检查
    # 如果将来有引用关系(如订单),可以在这里添加检查
    return True, ""
