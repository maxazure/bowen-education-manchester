from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.layout import PageLayout, PageLayoutSection, PageLayoutBlock, LayoutScope
from admin.app.blocks.registry import render_block


def get_layout(db: Session, scope: LayoutScope, scope_id: Optional[int] = None, status: Optional[str] = None) -> Optional[PageLayout]:
    q = select(PageLayout).where(PageLayout.scope == scope)
    if scope == LayoutScope.COLUMN:
        q = q.where(PageLayout.scope_id == scope_id)
    if status:
        q = q.where(PageLayout.status == status)
    return db.execute(q).scalars().first()


def get_or_create_draft(db: Session, scope: LayoutScope, scope_id: Optional[int] = None) -> PageLayout:
    layout = get_layout(db, scope, scope_id, status="draft")
    if not layout:
        layout = PageLayout(scope=scope, scope_id=scope_id, status="draft")
        db.add(layout)
        db.commit()
        db.refresh(layout)
    return layout


def read_layout_tree(db: Session, layout: PageLayout) -> Dict[str, Any]:
    sections = db.query(PageLayoutSection).filter_by(layout_id=layout.id).order_by(PageLayoutSection.sort_order).all()
    tree = []
    for s in sections:
        blocks = db.query(PageLayoutBlock).filter_by(section_id=s.id).order_by(PageLayoutBlock.sort_order).all()
        tree.append({
            "id": s.id,
            "title": s.title,
            "sort_order": s.sort_order,
            "is_enabled": s.is_enabled,
            "blocks": [
                {
                    "id": b.id,
                    "block_type": b.block_type,
                    "attributes_json": b.attributes_json,
                    "sort_order": b.sort_order,
                    "is_enabled": b.is_enabled,
                }
                for b in blocks
            ],
        })
    return {
        "layout": {
            "id": layout.id,
            "scope": layout.scope.value,
            "scope_id": layout.scope_id,
            "status": layout.status,
        },
        "sections": tree,
    }


def upsert_section(db: Session, layout_id: int, section_id: Optional[int], title: Optional[str], sort_order: Optional[int], is_enabled: Optional[bool]) -> PageLayoutSection:
    if section_id:
        s = db.query(PageLayoutSection).filter_by(id=section_id, layout_id=layout_id).first()
        if not s:
            raise ValueError("Section not found")
        if title is not None:
            s.title = title
        if sort_order is not None:
            s.sort_order = sort_order
        if is_enabled is not None:
            s.is_enabled = is_enabled
    else:
        s = PageLayoutSection(layout_id=layout_id, title=title or "", sort_order=sort_order or 0, is_enabled=is_enabled if is_enabled is not None else True)
        db.add(s)
    db.commit()
    db.refresh(s)
    return s


def reorder_sections(db: Session, layout_id: int, orders: List[Dict[str, int]]) -> int:
    count = 0
    for item in orders:
        s = db.query(PageLayoutSection).filter_by(id=item.get("id"), layout_id=layout_id).first()
        if s:
            s.sort_order = int(item.get("sort_order", s.sort_order))
            count += 1
    db.commit()
    return count


def upsert_block(db: Session, section_id: int, block_id: Optional[int], block_type: str, attributes_json: Optional[str], sort_order: Optional[int], is_enabled: Optional[bool]) -> PageLayoutBlock:
    if block_id:
        b = db.query(PageLayoutBlock).filter_by(id=block_id, section_id=section_id).first()
        if not b:
            raise ValueError("Block not found")
        b.block_type = block_type or b.block_type
        b.attributes_json = attributes_json if attributes_json is not None else b.attributes_json
        if sort_order is not None:
            b.sort_order = sort_order
        if is_enabled is not None:
            b.is_enabled = is_enabled
    else:
        b = PageLayoutBlock(section_id=section_id, block_type=block_type, attributes_json=attributes_json or "{}", sort_order=sort_order or 0, is_enabled=is_enabled if is_enabled is not None else True)
        db.add(b)
    db.commit()
    db.refresh(b)
    return b


def reorder_blocks(db: Session, section_id: int, orders: List[Dict[str, int]]) -> int:
    count = 0
    for item in orders:
        b = db.query(PageLayoutBlock).filter_by(id=item.get("id"), section_id=section_id).first()
        if b:
            b.sort_order = int(item.get("sort_order", b.sort_order))
            count += 1
    db.commit()
    return count


def publish_layout(db: Session, layout_id: int) -> PageLayout:
    from datetime import datetime
    layout = db.query(PageLayout).filter_by(id=layout_id).first()
    if not layout:
        raise ValueError("Layout not found")
    layout.status = "published"
    layout.published_at = datetime.utcnow()
    db.commit()
    db.refresh(layout)
    return layout


def render_layout_html(db: Session, layout: PageLayout) -> str:
    html_parts: List[str] = []
    sections = db.query(PageLayoutSection).filter_by(layout_id=layout.id, is_enabled=True).order_by(PageLayoutSection.sort_order).all()
    for s in sections:
        blocks = db.query(PageLayoutBlock).filter_by(section_id=s.id, is_enabled=True).order_by(PageLayoutBlock.sort_order).all()
        for b in blocks:
            # attributes_json -> dict
            import json
            try:
                attrs = json.loads(b.attributes_json) if b.attributes_json else {}
            except Exception:
                attrs = {}
            frag = render_block(b.block_type, attrs, db)
            if frag:
                html_parts.append(frag)
    return "\n".join(html_parts)