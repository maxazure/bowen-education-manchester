# -*- coding: utf-8 -*-
"""Template Helper Functions

These functions are available in Jinja2 templates
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Post, Product, SiteColumn
from app.services import post_service, product_service, site_service


def product_list(
    db: Session,
    column_id: Optional[int] = None,
    is_recommended: Optional[bool] = None,
    limit: Optional[int] = None,
    category_id: Optional[int] = None,
) -> List[Product]:
    """
    Template function: Get product list

    Usage in template:
        {% for product in product_list(is_recommended=True, limit=6) %}
            ...
        {% endfor %}

    Args:
        db: Database session
        column_id: Filter by column ID
        is_recommended: Filter by recommended products
        limit: Maximum number of products
        category_id: Filter by category ID

    Returns:
        List of products
    """
    return product_service.get_products(
        db=db,
        column_id=column_id,
        category_id=category_id,
        is_recommended=is_recommended,
        limit=limit,
    )


def post_list(
    db: Session,
    column_id: Optional[int] = None,
    is_recommended: Optional[bool] = None,
    limit: Optional[int] = None,
    category_id: Optional[int] = None,
) -> List[Post]:
    """
    Template function: Get post list

    Usage in template:
        {% for post in post_list(is_recommended=True, limit=3) %}
            ...
        {% endfor %}

    Args:
        db: Database session
        column_id: Filter by column ID
        is_recommended: Filter by recommended posts
        limit: Maximum number of posts
        category_id: Filter by category ID

    Returns:
        List of posts
    """
    return post_service.get_posts(
        db=db,
        column_id=column_id,
        category_id=category_id,
        is_recommended=is_recommended,
        limit=limit,
    )


def site_info(db: Session, key: str) -> Optional[str]:
    """
    Template function: Get site setting value

    Usage in template:
        {{ site_info('phone') }}
        {{ site_info('address') }}

    Args:
        db: Database session
        key: Setting key

    Returns:
        Setting value or None
    """
    return site_service.get_site_setting(db, key)


def get_navigation(db: Session, menu_location: Optional[str] = None) -> List[SiteColumn]:
    """
    Template function: Get navigation menu

    Usage in template:
        {# Get header navigation #}
        {% for nav_item in get_navigation('header') %}
            <a href="/{{ nav_item.slug }}">{{ nav_item.name }}</a>
        {% endfor %}

        {# Get footer navigation #}
        {% for nav_item in get_navigation('footer') %}
            <a href="/{{ nav_item.slug }}">{{ nav_item.name }}</a>
        {% endfor %}

    Args:
        db: Database session
        menu_location: Optional menu location filter ('header', 'footer', 'both')

    Returns:
        List of navigation items
    """
    return site_service.get_navigation(db, menu_location)
