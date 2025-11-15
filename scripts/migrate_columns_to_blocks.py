#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.site import SiteColumn, ColumnType
from app.models.layout import PageLayout, PageLayoutSection, PageLayoutBlock, LayoutScope
from app.services import site_service
import json


def get_or_create_layout(db: Session, column_id: int) -> PageLayout:
    layout = (
        db.query(PageLayout)
        .filter(PageLayout.scope == LayoutScope.COLUMN, PageLayout.scope_id == column_id)
        .order_by(PageLayout.id.asc())
        .first()
    )
    if not layout:
        layout = PageLayout(scope=LayoutScope.COLUMN, scope_id=column_id, status="draft")
        db.add(layout)
        db.commit(); db.refresh(layout)
    return layout


def clear_layout(db: Session, layout_id: int):
    db.query(PageLayoutBlock).filter(PageLayoutBlock.section_id.in_(
        db.query(PageLayoutSection.id).filter(PageLayoutSection.layout_id == layout_id)
    )).delete(synchronize_session=False)
    db.query(PageLayoutSection).filter(PageLayoutSection.layout_id == layout_id).delete(synchronize_session=False)
    db.commit()


def hero_banner_from_column(col: SiteColumn) -> dict:
    bg = col.hero_media.file_url if getattr(col, "hero_media", None) else ""
    return {
        "title": col.hero_title or (col.name or ""),
        "subtitle": col.hero_title_en or (col.hero_tagline or ""),
        "background_url": bg,
        "cta_text": col.hero_cta_text or "",
        "cta_link": col.hero_cta_url or f"/{col.slug}",
    }


def migrate_column(db: Session, col: SiteColumn):
    layout = get_or_create_layout(db, col.id)
    clear_layout(db, layout.id)

    # Section 1: Hero (if configured)
    hb = hero_banner_from_column(col)
    if any([hb.get("title"), hb.get("subtitle"), hb.get("background_url"), hb.get("cta_text")]):
        s1 = PageLayoutSection(layout_id=layout.id, title=f"{col.slug}-hero", sort_order=0, is_enabled=True)
        db.add(s1); db.commit(); db.refresh(s1)
        db.add(PageLayoutBlock(section_id=s1.id, block_type="HeroBanner", attributes_json=json.dumps(hb), sort_order=0, is_enabled=True))
        db.commit()

    order = 1
    # Section by type
    if col.column_type == ColumnType.SINGLE_PAGE:
        page = site_service.get_single_page(db, col.id)
        if page and page.content_html:
            s = PageLayoutSection(layout_id=layout.id, title=f"{col.slug}-page", sort_order=order, is_enabled=True)
            db.add(s); db.commit(); db.refresh(s)
            db.add(PageLayoutBlock(section_id=s.id, block_type="RichText", attributes_json=json.dumps({"html": page.content_html}), sort_order=0, is_enabled=True))
            db.commit(); order += 1
    elif col.column_type == ColumnType.POST:
        s = PageLayoutSection(layout_id=layout.id, title=f"{col.slug}-posts", sort_order=order, is_enabled=True)
        db.add(s); db.commit(); db.refresh(s)
        db.add(PageLayoutBlock(section_id=s.id, block_type="PostList", attributes_json=json.dumps({"column_id": col.id, "limit": 9}), sort_order=0, is_enabled=True))
        db.commit(); order += 1
    elif col.column_type == ColumnType.PRODUCT:
        s = PageLayoutSection(layout_id=layout.id, title=f"{col.slug}-products", sort_order=order, is_enabled=True)
        db.add(s); db.commit(); db.refresh(s)
        db.add(PageLayoutBlock(section_id=s.id, block_type="ProductGrid", attributes_json=json.dumps({"column_id": col.id, "limit": 9}), sort_order=0, is_enabled=True))
        db.commit(); order += 1
    elif col.column_type == ColumnType.GALLERY:
        s = PageLayoutSection(layout_id=layout.id, title=f"{col.slug}-gallery", sort_order=order, is_enabled=True)
        db.add(s); db.commit(); db.refresh(s)
        db.add(PageLayoutBlock(section_id=s.id, block_type="GalleryGrid", attributes_json=json.dumps({"limit": 12}), sort_order=0, is_enabled=True))
        db.commit(); order += 1
    elif col.column_type == ColumnType.CUSTOM:
        # If has child columns, create quick entry grid from children
        children = site_service.get_child_columns(db, col.id)
        if children:
            items = [{
                "title": c.name,
                "subtitle": c.slug,
                "desc": c.description or "",
                "href": f"/{c.slug}",
                "icon": "➡️",
                "tags": []
            } for c in children]
            s = PageLayoutSection(layout_id=layout.id, title=f"{col.slug}-overview", sort_order=order, is_enabled=True)
            db.add(s); db.commit(); db.refresh(s)
            db.add(PageLayoutBlock(section_id=s.id, block_type="QuickEntryGrid", attributes_json=json.dumps({"items": items}), sort_order=0, is_enabled=True))
            db.commit(); order += 1

    # Finalize as draft
    layout.status = "draft"
    db.commit()


def migrate_all(db: Session):
    cols = db.query(SiteColumn).filter(SiteColumn.is_enabled.is_(True)).order_by(SiteColumn.sort_order).all()
    for col in cols:
        migrate_column(db, col)
        print(f"[migrate] Column {col.slug} drafted as blocks")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        migrate_all(db)
        print("[migrate] All enabled columns drafted.")
    finally:
        db.close()