# -*- coding: utf-8 -*-
"""Post Service - Posts and categories"""

from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models import Post, PostCategory, PostCategoryLink
from app.utils.cache import cache_content


@cache_content
def get_post_categories(
    db: Session, column_id: int, visible_only: bool = True
) -> List[PostCategory]:
    """
    Get post categories for a column (cached for 5 minutes)

    Args:
        db: Database session
        column_id: Column ID
        visible_only: Only return visible categories

    Returns:
        List of PostCategory objects
    """
    query = db.query(PostCategory).filter(PostCategory.column_id == column_id)

    if visible_only:
        query = query.filter(PostCategory.is_visible == True)

    return query.order_by(PostCategory.sort_order).all()


@cache_content
def get_posts(
    db: Session,
    column_id: Optional[int] = None,
    category_id: Optional[int] = None,
    is_recommended: Optional[bool] = None,
    is_approved: Optional[bool] = None,
    status: str = "published",
    limit: Optional[int] = None,
    offset: int = 0,
) -> List[Post]:
    """
    Get posts with filters (cached for 5 minutes)

    Args:
        db: Database session
        column_id: Filter by column ID
        category_id: Filter by category ID
        is_recommended: Filter by recommended status
        is_approved: Filter by approval status
        status: Filter by status (default: published)
        limit: Maximum number of posts to return
        offset: Number of posts to skip

    Returns:
        List of Post objects
    """
    query = (
        db.query(Post)
        .options(joinedload(Post.cover_media))
        .filter(Post.status == status)
    )

    if column_id:
        query = query.filter(Post.column_id == column_id)

    if category_id:
        query = query.join(Post.categories).filter(PostCategory.id == category_id)

    if is_recommended is not None:
        query = query.filter(Post.is_recommended == is_recommended)

    if is_approved is not None:
        query = query.filter(Post.is_approved == is_approved)
    query = query.order_by(Post.published_at.desc(), Post.id.desc())

    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(limit)

    return query.all()


def get_post_by_slug(
    db: Session, slug: str, status: str = "published"
) -> Optional[Post]:
    """
    Get post by slug

    Args:
        db: Database session
        slug: Post slug
        status: Filter by status

    Returns:
        Post object or None
    """
    return (
        db.query(Post)
        .options(
            joinedload(Post.cover_media),
            joinedload(Post.categories),
        )
        .filter(Post.slug == slug, Post.status == status)
        .first()
    )


def get_post_count(
    db: Session,
    column_id: Optional[int] = None,
    category_id: Optional[int] = None,
    status: str = "published",
    is_approved: Optional[bool] = None,
) -> int:
    """
    Get post count

    Args:
        db: Database session
        column_id: Filter by column ID
        category_id: Filter by category ID
        status: Filter by status

    Returns:
        Number of posts
    """
    query = db.query(Post).filter(Post.status == status)
    if is_approved is not None:
        query = query.filter(Post.is_approved == is_approved)

    if column_id:
        query = query.filter(Post.column_id == column_id)

    if category_id:
        query = query.join(Post.categories).filter(PostCategory.id == category_id)

    return query.count()


def get_popular_posts(
    db: Session, column_id: Optional[int] = None, limit: int = 5
) -> List[Post]:
    """
    Get popular posts (for now, returns most recent posts as a placeholder)

    Args:
        db: Database session
        column_id: Filter by column ID
        limit: Maximum number of posts to return

    Returns:
        List of popular Post objects
    """
    query = (
        db.query(Post)
        .options(joinedload(Post.cover_media))
        .filter(Post.status == "published")
    )

    if column_id:
        query = query.filter(Post.column_id == column_id)

    return query.order_by(Post.published_at.desc()).limit(limit).all()


def get_category_stats(db: Session, column_id: Optional[int] = None) -> List[dict]:
    """
    Get post count by category

    Args:
        db: Database session
        column_id: Filter by column ID

    Returns:
        List of category stats with post counts
    """
    query = (
        db.query(
            PostCategory.id,
            PostCategory.name,
            PostCategory.slug,
            func.count(Post.id).label("post_count"),
        )
        .join(PostCategoryLink, PostCategory.id == PostCategoryLink.category_id)
        .join(Post, Post.id == PostCategoryLink.post_id)
        .filter(Post.status == "published")
        .filter(PostCategory.is_visible == True)
    )

    if column_id:
        query = query.filter(PostCategory.column_id == column_id)

    results = query.group_by(
        PostCategory.id, PostCategory.name, PostCategory.slug
    ).all()

    # Convert to list of dictionaries for template compatibility
    return [
        {
            "id": result.id,
            "name": result.name,
            "slug": result.slug,
            "post_count": result.post_count,
        }
        for result in results
    ]


def get_popular_tags(
    db: Session, column_id: Optional[int] = None, limit: int = 20
) -> List[str]:
    """
    Get popular tags from posts (placeholder implementation)

    Args:
        db: Database session
        column_id: Filter by column ID
        limit: Maximum number of tags to return

    Returns:
        List of popular tags
    """
    # For now, return a curated list of relevant tags
    # In a real implementation, this would extract tags from post content or a tags table
    default_tags = [
        "Smart Hydroponics",
        "Soilless Cultivation",
        "Modern Agriculture",
        "IoT Farming",
        "Energy Saving",
        "Green Farming",
        "Automation",
        "Nutrient Solution",
        "Indoor Growing",
        "Vertical Farming",
        "LED Growing",
        "Climate Control",
        "Urban Agriculture",
        "Sustainable Farming",
        "Water Conservation",
    ]

    return default_tags[:limit]
