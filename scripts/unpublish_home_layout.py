#!/usr/bin/env python3
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.layout import PageLayout, LayoutScope

def unpublish_home(db: Session):
    layout = (
        db.query(PageLayout)
        .filter(PageLayout.scope == LayoutScope.HOME, PageLayout.status == "published")
        .order_by(PageLayout.published_at.desc())
        .first()
    )
    if layout:
        layout.status = "draft"
        layout.published_at = None
        db.commit()
        print(f"[unpublish] Layout {layout.id} set to draft")
    else:
        print("[unpublish] No published home layout found")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        unpublish_home(db)
    finally:
        db.close()