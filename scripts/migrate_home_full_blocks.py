#!/usr/bin/env python3
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.layout import PageLayout, PageLayoutSection, PageLayoutBlock, LayoutScope
import json

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

def clear_layout(db: Session, layout_id: int):
    db.query(PageLayoutBlock).filter(PageLayoutBlock.section_id.in_(
        db.query(PageLayoutSection.id).filter(PageLayoutSection.layout_id == layout_id)
    )).delete(synchronize_session=False)
    db.query(PageLayoutSection).filter(PageLayoutSection.layout_id == layout_id).delete(synchronize_session=False)
    db.commit()

def migrate(db: Session):
    layout = ensure_home_layout(db)
    clear_layout(db, layout.id)

    hero_items = [
        {
            "title": "Bowen Education Group",
            "subtitle": "博文教育集团",
            "desc": "Bridging East and West Through Education",
            "background_url": "/static/images/heroes/hero-main-brand.jpg",
            "cta_text": "探索课程 Explore Courses",
            "cta_link": "/school/",
        },
        {
            "title": "Official HAF Programme Provider",
            "subtitle": "政府认证HAF项目提供商",
            "desc": "Funded by Trafford Council - Free Holiday Activities & Healthy Food",
            "background_url": "/static/images/heroes/hero-haf-programme.jpg",
            "badge_text": "Trafford Council",
            "cta_text": "了解HAF项目 Learn More",
            "cta_link": "/programmes-haf/",
        },
        {
            "title": "Strategic Partnership with Henan University",
            "subtitle": "河南大学战略合作伙伴",
            "desc": "Cultural Exchange Programmes & Root-seeking Tours",
            "background_url": "/static/images/heroes/hero-henan-university.jpg",
            "badge_text": "河南大学",
            "cta_text": "查看合作详情 View Partnership",
            "cta_link": "/events-henan/",
        },
        {
            "title": "GCSE Chinese",
            "subtitle": "GCSE中文考试班",
            "desc": "Professional GCSE Chinese exam preparation",
            "background_url": "/static/images/heroes/hero-event-featured.jpg",
            "cta_text": "查看详情 View Courses",
            "cta_link": "/school/",
        },
    ]
    s1 = PageLayoutSection(layout_id=layout.id, title="HeroCarousel", sort_order=0, is_enabled=True)
    db.add(s1); db.commit(); db.refresh(s1)
    db.add(PageLayoutBlock(section_id=s1.id, block_type="HeroCarousel", attributes_json=json.dumps({"items": hero_items}), sort_order=0, is_enabled=True))
    db.commit()

    quick_items = [
        {"title":"中文学校","subtitle":"Chinese School","desc":"从基础到A-Level的全方位中文教育","href":"/school/","icon":"📚","tags":["GCSE中文","A-Level中文","HSK考试"]},
        {"title":"补习中心","subtitle":"Tuition Center","desc":"专业学科辅导，提升学业成绩","href":"/tuition/","icon":"🎯","tags":["数学辅导","英语辅导","科学辅导"]},
        {"title":"政府项目","subtitle":"Government Programmes","desc":"政府资助的社区教育服务","href":"/programmes/","icon":"🏛️","tags":["社区项目","免费课程","文化推广"]},
        {"title":"国际象棋","subtitle":"Chess Club","desc":"专业象棋培训，培养思维能力","href":"/chess/","icon":"♟️","tags":["ECF认证","比赛培训","青少年培训"]},
        {"title":"羽毛球俱乐部","subtitle":"Badminton Club","desc":"专业羽毛球训练，增强身体素质","href":"/badminton/","icon":"🏸","tags":["专业教练","俱乐部联赛","青少年培训"]},
        {"title":"活动动态","subtitle":"Events & Activities","desc":"丰富多彩的文化教育活动","href":"/events/","icon":"🎉","tags":["文化节","夏令营","比赛活动"]},
    ]
    s2 = PageLayoutSection(layout_id=layout.id, title="QuickEntry", sort_order=1, is_enabled=True)
    db.add(s2); db.commit(); db.refresh(s2)
    db.add(PageLayoutBlock(section_id=s2.id, block_type="QuickEntryGrid", attributes_json=json.dumps({"items": quick_items, "heading_badge": "Quick Access / 快捷入口", "heading_title": "Explore Our Services", "heading_subtitle": "快速访问我们的主要服务项目"}), sort_order=0, is_enabled=True))
    db.commit()

    service_items = [
        {"title":"Chinese School","subtitle":"中文学校","desc":"From Foundation to A-Level Mandarin, HSK, YCT","href":"/school/","icon":"📚","background_url":"/static/images/services/service-chinese-school.jpg"},
        {"title":"Chess Club","subtitle":"国际象棋俱乐部","desc":"ECF-affiliated club for all levels","href":"/chess/","icon":"♟️","background_url":"/static/images/services/service-chess-club.jpg"},
        {"title":"Badminton Club","subtitle":"羽毛球俱乐部","desc":"Professional coaching for juniors and adults","href":"/badminton/","icon":"🏸","background_url":"/static/images/services/service-badminton-club.jpg"},
        {"title":"Government Programmes","subtitle":"政府项目","desc":"HAF programme funded by Trafford Council","href":"/programmes/","icon":"🏛️","background_url":"/static/images/services/service-government-programmes.jpg","badge_text":"FREE 免费"},
    ]
    s3 = PageLayoutSection(layout_id=layout.id, title="ServiceBlocks", sort_order=2, is_enabled=True)
    db.add(s3); db.commit(); db.refresh(s3)
    db.add(PageLayoutBlock(section_id=s3.id, block_type="ServiceBlocksGrid", attributes_json=json.dumps({"items": service_items, "heading_badge": "Our Services / 服务项目", "heading_title": "Comprehensive Education Solutions", "heading_subtitle": "为不同年龄和需求提供多元化教育服务"}), sort_order=0, is_enabled=True))
    db.commit()

    s4 = PageLayoutSection(layout_id=layout.id, title="NewsGrid", sort_order=3, is_enabled=True)
    db.add(s4); db.commit(); db.refresh(s4)
    db.add(PageLayoutBlock(section_id=s4.id, block_type="NewsGrid", attributes_json=json.dumps({"limit": 6, "heading_badge": "Latest Updates / 最新动态", "heading_title": "News & Events", "heading_subtitle": "Stay updated with our latest activities and announcements", "view_all": True, "view_all_href": "/news/"}), sort_order=0, is_enabled=True))
    db.commit()

    logos = []
    names = [
        "University of Bolton",
        "Manchester City Council",
    ]
    s5 = PageLayoutSection(layout_id=layout.id, title="Partners", sort_order=4, is_enabled=True)
    db.add(s5); db.commit(); db.refresh(s5)
    db.add(PageLayoutBlock(section_id=s5.id, block_type="PartnerLogos", attributes_json=json.dumps({"logos": logos, "names": names, "heading_title": "The Organisations Who Trust Us"}), sort_order=0, is_enabled=True))
    db.commit()

    s6 = PageLayoutSection(layout_id=layout.id, title="Stats", sort_order=5, is_enabled=True)
    db.add(s6); db.commit(); db.refresh(s6)
    db.add(PageLayoutBlock(section_id=s6.id, block_type="StatsSection", attributes_json=json.dumps({"heading_title": "Our Achievements / 我们的成就", "heading_subtitle": "Building excellence in education since 2018"}), sort_order=0, is_enabled=True))
    db.commit()

    s7 = PageLayoutSection(layout_id=layout.id, title="Contact", sort_order=6, is_enabled=True)
    db.add(s7); db.commit(); db.refresh(s7)
    db.add(PageLayoutBlock(section_id=s7.id, block_type="ContactSection", attributes_json=json.dumps({"enable_form": True, "heading_badge": "Get in Touch / 联系我们", "heading_title": "We're Here to Help", "heading_subtitle": "Have questions? We'd love to hear from you"}), sort_order=0, is_enabled=True))
    db.commit()

    from datetime import datetime
    layout.status = "published"
    layout.published_at = datetime.utcnow()
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        migrate(db)
        print("[migrate] Homepage full blocks drafted.")
    finally:
        db.close()