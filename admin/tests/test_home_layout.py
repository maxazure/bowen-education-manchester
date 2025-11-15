from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.layout import PageLayout, PageLayoutSection, PageLayoutBlock, LayoutScope
from admin.app.services.layout_service import render_layout_html


def test_render_layout_html_basic():
    db: Session = SessionLocal()
    try:
        # 创建草稿布局与一个分区、一个 RichText 区块
        layout = PageLayout(scope=LayoutScope.HOME, status="draft")
        db.add(layout)
        db.commit(); db.refresh(layout)

        section = PageLayoutSection(layout_id=layout.id, title="测试", sort_order=0, is_enabled=True)
        db.add(section); db.commit(); db.refresh(section)

        block = PageLayoutBlock(section_id=section.id, block_type="RichText", attributes_json='{"html":"<p>你好，测试！</p>"}', sort_order=0, is_enabled=True)
        db.add(block); db.commit()

        html = render_layout_html(db, layout)
        assert "你好，测试！" in html
    finally:
        db.close()