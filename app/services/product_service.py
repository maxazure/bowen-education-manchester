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
        query = query.filter(ProductCategory.is_visible == True)

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
