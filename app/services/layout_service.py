from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.layout import PageLayout, PageLayoutSection, PageLayoutBlock, LayoutScope
from admin.app.blocks.registry import render_block


def get_published_layout(db: Session, scope: LayoutScope, scope_id: Optional[int] = None) -> Optional[PageLayout]:
    q = db.query(PageLayout).filter(PageLayout.scope == scope, PageLayout.status == "published")
    if scope == LayoutScope.COLUMN:
        q = q.filter(PageLayout.scope_id == scope_id)
    return q.order_by(PageLayout.published_at.desc()).first()


def render_layout_html(db: Session, layout: PageLayout) -> str:
    parts: List[str] = []
    sections = db.query(PageLayoutSection).filter_by(layout_id=layout.id, is_enabled=True).order_by(PageLayoutSection.sort_order).all()
    for s in sections:
        blocks = db.query(PageLayoutBlock).filter_by(section_id=s.id, is_enabled=True).order_by(PageLayoutBlock.sort_order).all()
        for b in blocks:
            import json
            try:
                attrs = json.loads(b.attributes_json) if b.attributes_json else {}
            except Exception:
                attrs = {}
            frag = render_block(b.block_type, attrs, db)
            if frag:
                parts.append(frag)
    return "\n".join(parts)