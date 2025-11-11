# -*- coding: utf-8 -*-
"""Site Service - Site columns, settings, single pages"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import SinglePage, SiteColumn, SiteSetting, MenuLocation
from app.utils.cache import cache_navigation, cache_settings


@cache_navigation
def get_navigation(db: Session, menu_location: Optional[str] = None) -> List[SiteColumn]:
    """
    Get navigation menu items (cached for 10 minutes)

    Returns all enabled columns including children for building
    multi-level navigation menus

    Args:
        db: Database session
        menu_location: Optional menu location filter ('header', 'footer', 'both')
                      If None, returns all enabled columns
                      If specified, returns columns for that location or 'both'

    Returns:
        List of all enabled columns (both parent and child columns)
    """
    query = db.query(SiteColumn).filter(SiteColumn.is_enabled == True)

    # Filter by menu location if specified
    if menu_location:
        # Normalize to uppercase and filter by menu_location (DB stores uppercase enum values)
        menu_location_upper = menu_location.upper()
        # Include columns that match the location or are set to 'BOTH'
        query = query.filter(
            (SiteColumn.menu_location == menu_location_upper) |
            (SiteColumn.menu_location == "BOTH")
        )

    return query.order_by(SiteColumn.sort_order).all()


def get_column_by_slug(db: Session, slug: str) -> Optional[SiteColumn]:
    """
    Get column by slug

    Args:
        db: Database session
        slug: Column slug

    Returns:
        SiteColumn object or None
    """
    return (
        db.query(SiteColumn)
        .filter(SiteColumn.slug == slug, SiteColumn.is_enabled == True)
        .first()
    )


def get_single_page(db: Session, column_id: int) -> Optional[SinglePage]:
    """
    Get single page by column ID

    Args:
        db: Database session
        column_id: Column ID

    Returns:
        SinglePage object or None
    """
    return (
        db.query(SinglePage)
        .filter(SinglePage.column_id == column_id, SinglePage.status == "published")
        .first()
    )


@cache_settings
def get_site_setting(db: Session, key: str) -> Optional[str]:
    """
    Get site setting value by key (cached for 10 minutes)

    Args:
        db: Database session
        key: Setting key

    Returns:
        Setting value or None
    """
    setting = db.query(SiteSetting).filter(SiteSetting.setting_key == key).first()
    return setting.value_text if setting else None


@cache_settings
def get_all_site_settings(db: Session) -> dict:
    """
    Get all site settings as a dictionary (cached for 10 minutes)

    Args:
        db: Database session

    Returns:
        Dictionary of settings {key: value}
    """
    settings = db.query(SiteSetting).all()
    return {s.setting_key: s.value_text for s in settings}


def get_child_columns(db: Session, parent_id: int) -> List[SiteColumn]:
    """
    Get child columns for a parent column

    Args:
        db: Database session
        parent_id: Parent column ID

    Returns:
        List of child SiteColumn objects
    """
    return (
        db.query(SiteColumn)
        .filter(SiteColumn.parent_id == parent_id, SiteColumn.is_enabled == True)
        .order_by(SiteColumn.sort_order)
        .all()
    )


def get_overview_sections(db: Session, parent_column_id: int) -> List[dict]:
    """
    Get overview sections for a composite page

    Returns data from child columns to display as sections
    on a parent overview/composite page

    Args:
        db: Database session
        parent_column_id: Parent column ID

    Returns:
        List of section dictionaries with child column info and content
    """
    from app.services import post_service, product_service

    sections = []
    child_columns = get_child_columns(db, parent_column_id)

    for child in child_columns:
        section = {
            "column": child,
            "column_name": child.name,
            "column_slug": child.slug,
            "column_type": child.column_type,
            "content_items": [],
            "content": None,
        }

        # Get content based on column type
        if child.column_type == "POST":
            # Get latest posts from this child column
            posts = post_service.get_posts(
                db,
                column_id=child.id,
                limit=6
            )
            section["content_items"] = posts

        elif child.column_type == "PRODUCT":
            # Get products from this child column
            products = product_service.get_products(
                db,
                column_id=child.id,
                limit=6
            )
            section["content_items"] = products

        elif child.column_type == "SINGLE_PAGE":
            # Get single page content
            single_page = get_single_page(db, child.id)
            section["content"] = single_page

        sections.append(section)

    return sections
