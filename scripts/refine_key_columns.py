#!/usr/bin/env python3
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.site import SiteColumn
from app.models.layout import PageLayout, PageLayoutSection, PageLayoutBlock, LayoutScope
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

def ensure_section(db: Session, layout_id: int, title: str, order: int) -> PageLayoutSection:
    s = PageLayoutSection(layout_id=layout_id, title=title, sort_order=order, is_enabled=True)
    db.add(s); db.commit(); db.refresh(s)
    return s

def hero_attrs(col: SiteColumn) -> dict:
    bg = col.hero_media.file_url if getattr(col, "hero_media", None) else ""
    return {
        "title": col.hero_title or (col.name or ""),
        "subtitle": col.hero_title_en or (col.hero_tagline or ""),
        "background_url": bg,
        "cta_text": col.hero_cta_text or "",
        "cta_link": col.hero_cta_url or f"/{col.slug}",
    }

def refine_column(db: Session, slug: str, with_news: bool = True, with_quick_children: bool = True, with_contact: bool = False):
    col = db.query(SiteColumn).filter(SiteColumn.slug == slug).first()
    if not col:
        return
    layout = get_or_create_layout(db, col.id)
    order = 0
    h = hero_attrs(col)
    if any([h.get("title"), h.get("subtitle"), h.get("background_url"), h.get("cta_text")]):
        s = ensure_section(db, layout.id, f"{slug}-hero", order); order += 1
        db.add(PageLayoutBlock(section_id=s.id, block_type="HeroBanner", attributes_json=json.dumps(h), sort_order=0, is_enabled=True)); db.commit()
    if with_quick_children:
        from app.services import site_service
        children = site_service.get_child_columns(db, col.id)
        if children:
            items = [{"title": c.name, "subtitle": c.slug, "desc": c.description or "", "href": f"/{c.slug}", "icon": "➡️", "tags": []} for c in children]
            s = ensure_section(db, layout.id, f"{slug}-overview", order); order += 1
            db.add(PageLayoutBlock(section_id=s.id, block_type="QuickEntryGrid", attributes_json=json.dumps({"items": items}), sort_order=0, is_enabled=True)); db.commit()
    if with_news:
        s = ensure_section(db, layout.id, f"{slug}-news", order); order += 1
        db.add(PageLayoutBlock(section_id=s.id, block_type="NewsGrid", attributes_json=json.dumps({"column_id": col.id, "limit": 6}), sort_order=0, is_enabled=True)); db.commit()
    if with_contact:
        s = ensure_section(db, layout.id, f"{slug}-contact", order); order += 1
        db.add(PageLayoutBlock(section_id=s.id, block_type="ContactSection", attributes_json=json.dumps({"enable_form": True}), sort_order=0, is_enabled=True)); db.commit()
    layout.status = "draft"; db.commit()

def main():
    db = SessionLocal()
    try:
        refine_column(db, "school", with_news=True, with_quick_children=True)
        refine_column(db, "chess", with_news=True, with_quick_children=True)
        refine_column(db, "badminton", with_news=True, with_quick_children=True)
        refine_column(db, "programmes", with_news=False, with_quick_children=True)
        refine_column(db, "contact", with_news=False, with_quick_children=False, with_contact=True)
        print("[refine] Key columns drafted with refined blocks.")
    finally:
        db.close()

if __name__ == "__main__":
    main()