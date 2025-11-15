#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
将当前首页模板的内容迁移为区块布局并发布：
- HeroBanner：最近推荐活动文章作为横幅
- PostList：最新 6 篇发布文章
- ProductGrid：推荐产品 6 个
- ContactCTA：联系我们

运行：
    source venv/bin/activate
    PYTHONPATH=. python scripts/migrate_home_template_to_blocks.py
"""

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services import site_service, post_service, product_service
from app.models.layout import PageLayout, PageLayoutSection, PageLayoutBlock, LayoutScope


def clear_layout(db: Session, layout_id: int):
    db.query(PageLayoutBlock).filter(PageLayoutBlock.section_id.in_(
        db.query(PageLayoutSection.id).filter(PageLayoutSection.layout_id == layout_id)
    )).delete(synchronize_session=False)
    db.query(PageLayoutSection).filter(PageLayoutSection.layout_id == layout_id).delete(synchronize_session=False)
    db.commit()


def ensure_home_layout(db: Session) -> PageLayout:
    layout = (
        db.query(PageLayout)
        .filter(PageLayout.scope == LayoutScope.HOME)
        .order_by(PageLayout.id.asc())
        .first()
    )
    if not layout:
        layout = PageLayout(scope=LayoutScope.HOME, status="draft")
        db.add(layout)
        db.commit(); db.refresh(layout)
    return layout


def migrate(db: Session):
    layout = ensure_home_layout(db)
    clear_layout(db, layout.id)

    # Section 1: HeroBanner from latest recommended event post
    hero_section = PageLayoutSection(layout_id=layout.id, title="Hero", sort_order=0, is_enabled=True)
    db.add(hero_section); db.commit(); db.refresh(hero_section)
    featured = post_service.get_posts(db, is_recommended=True, limit=1)
    if featured:
        p = featured[0]
        import json
        attrs = {
            "title": p.title,
            "subtitle": (p.summary or "")[:200],
            "background_url": getattr(p, "featured_image", ""),
            "cta_text": "查看详情",
            "cta_link": f"/{p.column.slug}/{p.slug}" if getattr(p, "column", None) else "/news",
        }
        db.add(PageLayoutBlock(section_id=hero_section.id, block_type="HeroBanner", attributes_json=json.dumps(attrs), sort_order=0, is_enabled=True))
        db.commit()

    # Section 2: Latest posts list
    posts_section = PageLayoutSection(layout_id=layout.id, title="Latest Posts", sort_order=1, is_enabled=True)
    db.add(posts_section); db.commit(); db.refresh(posts_section)
    import json
    db.add(PageLayoutBlock(section_id=posts_section.id, block_type="PostList", attributes_json=json.dumps({"limit": 6, "status": "published"}), sort_order=0, is_enabled=True))
    db.commit()

    # Section 3: Recommended products
    products_section = PageLayoutSection(layout_id=layout.id, title="Featured Products", sort_order=2, is_enabled=True)
    db.add(products_section); db.commit(); db.refresh(products_section)
    import json
    db.add(PageLayoutBlock(section_id=products_section.id, block_type="ProductGrid", attributes_json=json.dumps({"limit": 6, "is_recommended": True}), sort_order=0, is_enabled=True))
    db.commit()

    # Section 4: Contact CTA
    contact_section = PageLayoutSection(layout_id=layout.id, title="Contact", sort_order=3, is_enabled=True)
    db.add(contact_section); db.commit(); db.refresh(contact_section)
    db.add(PageLayoutBlock(section_id=contact_section.id, block_type="ContactCTA", attributes_json=json.dumps({"title": "需要帮助？联系我们", "button_text": "联系我们", "button_link": "/contact"}), sort_order=0, is_enabled=True))
    db.commit()

    # Publish layout
    layout.status = "published"
    from datetime import datetime
    layout.published_at = datetime.utcnow()
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        migrate(db)
        print("[migrate] Homepage template migrated into blocks and published.")
    finally:
        db.close()