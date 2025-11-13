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
        query = query.filter(PostCategory.is_visible.is_(True))

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
        .filter(PostCategory.is_visible.is_(True))
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


# ===== 管理后台功能 =====


def generate_slug(title: str, db: Session, exclude_id: Optional[int] = None) -> str:
    """
    生成唯一的 slug

    Args:
        title: 文章标题
        db: 数据库会话
        exclude_id: 排除的文章 ID (用于更新时)

    Returns:
        唯一的 slug
    """
    from app.services.single_page_service import slugify

    base_slug = slugify(title)

    if not base_slug:
        base_slug = "post"

    # 检查 slug 是否已存在
    query = db.query(Post).filter(Post.slug == base_slug)
    if exclude_id:
        query = query.filter(Post.id != exclude_id)

    existing = query.first()

    if not existing:
        return base_slug

    # 如果已存在,添加数字后缀
    counter = 1
    while True:
        new_slug = f"{base_slug}-{counter}"
        query = db.query(Post).filter(Post.slug == new_slug)
        if exclude_id:
            query = query.filter(Post.id != exclude_id)

        if not query.first():
            return new_slug

        counter += 1


def can_delete_post(db: Session, post_id: int) -> tuple[bool, str]:
    """
    检查文章是否可以删除

    Args:
        db: 数据库会话
        post_id: 文章 ID

    Returns:
        (是否可以删除, 错误消息)
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return False, "文章不存在"

    # 文章可以直接删除,无需特殊检查
    # 如果将来有引用关系(如评论),可以在这里添加检查
    return True, ""


def publish_post(db: Session, post_id: int) -> tuple[bool, str]:
    """
    发布文章

    Args:
        db: 数据库会话
        post_id: 文章 ID

    Returns:
        (是否成功, 消息)
    """
    from datetime import datetime

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return False, "文章不存在"

    if post.status == "published":
        return False, "文章已经是发布状态"

    post.status = "published"
    post.published_at = datetime.now()
    db.commit()

    return True, "发布成功"


def unpublish_post(db: Session, post_id: int) -> tuple[bool, str]:
    """
    取消发布文章

    Args:
        db: 数据库会话
        post_id: 文章 ID

    Returns:
        (是否成功, 消息)
    """
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return False, "文章不存在"

    if post.status == "draft":
        return False, "文章已经是草稿状态"

    post.status = "draft"
    db.commit()

    return True, "取消发布成功"
