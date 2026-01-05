#!/usr/bin/env python3
"""
创建初始Hero幻灯片数据
将现有的硬编码幻灯片迁移到数据库中
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.hero import HeroSlide


def seed_hero_slides():
    """创建初始Hero幻灯片数据"""
    db: Session = SessionLocal()

    try:
        # 检查是否已有数据
        existing_count = db.query(HeroSlide).count()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 个Hero幻灯片，跳过创建")
            return

        # 创建4个幻灯片
        heroes = [
            {
                "title": "Bowen Education Group",
                "title_en": "Bowen Education Group",
                "subtitle": "博文教育集团",
                "subtitle_en": "Bridging East and West Through Education",
                "description": "中西融汇，博学致远",
                "description_en": None,
                "background_image": "/static/images/heroes/hero-main-brand.jpg",
                "badge_text": None,
                "badge_text_en": None,
                "button_text": "探索课程 Explore Courses",
                "button_text_en": "Explore Courses",
                "button_url": "/school/",
                "button_style": "btn-primary",
                "button2_text": "预约试听 Book Trial",
                "button2_text_en": "Book Trial",
                "button2_url": "/contact/",
                "button2_style": "btn-outline-light",
                "sort_order": 10,
                "is_active": True,
            },
            {
                "title": "Official HAF Programme Provider",
                "title_en": "Official HAF Programme Provider",
                "subtitle": "政府认证HAF项目提供商",
                "subtitle_en": "Trafford Council Partnership",
                "description": "Funded by Trafford Council - Free Holiday Activities & Healthy Food for Eligible Children",
                "description_en": "Funded by Trafford Council - Free Holiday Activities & Healthy Food for Eligible Children",
                "background_image": "/static/images/heroes/hero-haf-programme.jpg",
                "badge_text": "Trafford Council",
                "badge_text_en": "Trafford Council",
                "button_text": "了解HAF项目 Learn More",
                "button_text_en": "Learn More",
                "button_url": "/programmes-haf/",
                "button_style": "btn-success",
                "button2_text": None,
                "button2_text_en": None,
                "button2_url": None,
                "button2_style": None,
                "sort_order": 20,
                "is_active": True,
            },
            {
                "title": "Strategic Partnership with Henan University",
                "title_en": "Strategic Partnership with Henan University",
                "subtitle": "河南大学战略合作伙伴",
                "subtitle_en": "International Education Partnership",
                "description": "Cultural Exchange Programmes & Root-seeking Tours to China",
                "description_en": "Cultural Exchange Programmes & Root-seeking Tours to China",
                "background_image": "/static/images/heroes/hero-henan-university.jpg",
                "badge_text": "河南大学",
                "badge_text_en": "Henan University",
                "button_text": "查看合作详情 View Partnership",
                "button_text_en": "View Partnership",
                "button_url": "/events-henan/",
                "button_style": "btn-warning",
                "button2_text": None,
                "button2_text_en": None,
                "button2_url": None,
                "button2_style": None,
                "sort_order": 30,
                "is_active": True,
            },
            {
                "title": "GCSE Chinese",
                "title_en": "GCSE Chinese",
                "subtitle": "GCSE中文考试班",
                "subtitle_en": "Professional Exam Preparation",
                "description": "Professional GCSE Chinese exam preparation - Qualified teachers & Proven results",
                "description_en": "Professional GCSE Chinese exam preparation - Qualified teachers & Proven results",
                "background_image": "/static/images/heroes/hero-event-featured.jpg",
                "badge_text": None,
                "badge_text_en": None,
                "button_text": "查看详情 View Courses",
                "button_text_en": "View Courses",
                "button_url": "/school/",
                "button_style": "btn-primary",
                "button2_text": None,
                "button2_text_en": None,
                "button2_url": None,
                "button2_style": None,
                "sort_order": 40,
                "is_active": True,
            },
        ]

        # 插入数据
        for hero_data in heroes:
            hero = HeroSlide(**hero_data)
            db.add(hero)

        db.commit()
        print(f"✅ 成功创建 {len(heroes)} 个Hero幻灯片")

        # 显示创建的幻灯片
        print("\n创建的幻灯片:")
        for i, hero_data in enumerate(heroes, 1):
            print(f"{i}. {hero_data['title']} (排序: {hero_data['sort_order']})")

    except Exception as e:
        print(f"❌ 创建Hero幻灯片失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_hero_slides()
