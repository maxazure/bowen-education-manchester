#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量翻译中文内容到英文
自动为所有空的英文字段填充翻译内容
"""

import sqlite3
import re
from typing import Dict, List, Tuple

# 简单的中英文对照词典（针对教育领域）
TRANSLATION_DICT = {
    # 通用词汇
    "博文教育集团": "Bowen Education Group",
    "博文集团": "Bowen Education Group",
    "曼彻斯特": "Manchester",
    "中文": "Chinese",
    "汉语": "Chinese Language",
    "英国": "UK",
    "河南大学": "Henan University",

    # 课程相关
    "课程": "Course",
    "班级": "Class",
    "学期": "Semester",
    "招生": "Enrollment",
    "报名": "Registration",
    "学费": "Tuition Fee",
    "教学": "Teaching",
    "学习": "Learning",
    "考试": "Examination",
    "测试": "Test",
    "模拟": "Mock",
    "水平": "Level",
    "基础": "Foundation",
    "启蒙": "Beginner",
    "进阶": "Advanced",

    # 活动相关
    "活动": "Event",
    "庆祝": "Celebration",
    "联欢": "Gathering",
    "晚会": "Gala",
    "训练营": "Training Camp",
    "夏季": "Summer",
    "春节": "Chinese New Year",
    "新年": "New Year",
    "国际象棋": "Chess",

    # 时间词汇
    "年": "Year",
    "月": "Month",
    "日": "Day",
    "秋季": "Autumn",
    "春季": "Spring",
    "冬季": "Winter",

    # 其他
    "项目": "Program",
    "圆满结束": "Successfully Concluded",
    "现已开放": "Now Open",
    "战略合作": "Strategic Partnership",
    "伙伴关系": "Partnership",
    "建立": "Establish",
    "佳绩": "Excellent Results",
    "获得": "Achieve",
}


def simple_translate(text: str) -> str:
    """
    简单的词典翻译（替换已知词汇）
    注意：这只是一个基础翻译，建议后续人工审核
    """
    if not text or text.strip() == "":
        return ""

    # 如果已经是英文，直接返回
    if re.search(r'^[a-zA-Z0-9\s\-\(\)\/,.!?:]+$', text):
        return text

    translated = text

    # 按词典替换
    for zh, en in TRANSLATION_DICT.items():
        translated = translated.replace(zh, en)

    return translated


def translate_products(conn: sqlite3.Connection) -> int:
    """翻译产品数据"""
    cursor = conn.cursor()

    # 获取所有需要翻译的产品
    cursor.execute("""
        SELECT id, name, summary, description_html, price_text,
               seo_title, seo_description
        FROM product
        WHERE name_en IS NULL OR name_en = ''
    """)

    products = cursor.fetchall()
    count = 0

    for product in products:
        product_id, name, summary, desc_html, price, seo_title, seo_desc = product

        # 翻译各个字段
        name_en = simple_translate(name) if name else ""
        summary_en = simple_translate(summary) if summary else ""

        # HTML 内容需要保留标签，只翻译文本
        if desc_html:
            # 简单处理：提取文本翻译后再包装
            desc_text = re.sub(r'<[^>]+>', '', desc_html)
            desc_en = simple_translate(desc_text)
            desc_html_en = f"<p>{desc_en}</p>" if desc_en else ""
        else:
            desc_html_en = ""

        price_text_en = simple_translate(price) if price else ""
        seo_title_en = simple_translate(seo_title) if seo_title else name_en
        seo_desc_en = simple_translate(seo_desc) if seo_desc else summary_en

        # 更新数据库
        cursor.execute("""
            UPDATE product
            SET name_en = ?,
                summary_en = ?,
                description_html_en = ?,
                price_text_en = ?,
                seo_title_en = ?,
                seo_description_en = ?
            WHERE id = ?
        """, (name_en, summary_en, desc_html_en, price_text_en,
              seo_title_en, seo_desc_en, product_id))

        count += 1
        print(f"✓ 产品 #{product_id}: {name} → {name_en}")

    conn.commit()
    return count


def translate_posts(conn: sqlite3.Connection) -> int:
    """翻译文章数据"""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, summary, content_html, seo_title, seo_description
        FROM post
        WHERE title_en IS NULL OR title_en = ''
    """)

    posts = cursor.fetchall()
    count = 0

    for post in posts:
        post_id, title, summary, content_html, seo_title, seo_desc = post

        title_en = simple_translate(title) if title else ""
        summary_en = simple_translate(summary) if summary else ""

        # HTML 内容翻译
        if content_html:
            content_text = re.sub(r'<[^>]+>', '', content_html)
            content_en = simple_translate(content_text)
            content_html_en = f"<p>{content_en}</p>" if content_en else ""
        else:
            content_html_en = ""

        seo_title_en = simple_translate(seo_title) if seo_title else title_en
        seo_desc_en = simple_translate(seo_desc) if seo_desc else summary_en

        cursor.execute("""
            UPDATE post
            SET title_en = ?,
                summary_en = ?,
                content_html_en = ?,
                seo_title_en = ?,
                seo_description_en = ?
            WHERE id = ?
        """, (title_en, summary_en, content_html_en, seo_title_en,
              seo_desc_en, post_id))

        count += 1
        print(f"✓ 文章 #{post_id}: {title} → {title_en}")

    conn.commit()
    return count


def translate_events(conn: sqlite3.Connection) -> int:
    """翻译活动数据"""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, description, summary, venue_name,
               seo_title, seo_description
        FROM event
        WHERE title_en IS NULL OR title_en = ''
    """)

    events = cursor.fetchall()
    count = 0

    for event in events:
        event_id, title, desc, summary, venue, seo_title, seo_desc = event

        title_en = simple_translate(title) if title else ""
        description_en = simple_translate(desc) if desc else ""
        summary_en = simple_translate(summary) if summary else ""
        venue_name_en = simple_translate(venue) if venue else ""
        seo_title_en = simple_translate(seo_title) if seo_title else title_en
        seo_desc_en = simple_translate(seo_desc) if seo_desc else summary_en

        cursor.execute("""
            UPDATE event
            SET title_en = ?,
                description_en = ?,
                summary_en = ?,
                venue_name_en = ?,
                seo_title_en = ?,
                seo_description_en = ?
            WHERE id = ?
        """, (title_en, description_en, summary_en, venue_name_en,
              seo_title_en, seo_desc_en, event_id))

        count += 1
        print(f"✓ 活动 #{event_id}: {title} → {title_en}")

    conn.commit()
    return count


def translate_single_pages(conn: sqlite3.Connection) -> int:
    """翻译单页数据"""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, subtitle, content_html, seo_title, seo_description
        FROM single_page
        WHERE title_en IS NULL OR title_en = ''
    """)

    pages = cursor.fetchall()
    count = 0

    for page in pages:
        page_id, title, subtitle, content_html, seo_title, seo_desc = page

        title_en = simple_translate(title) if title else ""
        subtitle_en = simple_translate(subtitle) if subtitle else ""

        # HTML 内容翻译
        if content_html:
            content_text = re.sub(r'<[^>]+>', '', content_html)
            content_en = simple_translate(content_text)
            content_html_en = f"<p>{content_en}</p>" if content_en else ""
        else:
            content_html_en = ""

        seo_title_en = simple_translate(seo_title) if seo_title else title_en
        seo_desc_en = simple_translate(seo_desc) if seo_desc else subtitle_en

        cursor.execute("""
            UPDATE single_page
            SET title_en = ?,
                subtitle_en = ?,
                content_html_en = ?,
                seo_title_en = ?,
                seo_description_en = ?
            WHERE id = ?
        """, (title_en, subtitle_en, content_html_en, seo_title_en,
              seo_desc_en, page_id))

        count += 1
        print(f"✓ 单页 #{page_id}: {title} → {title_en}")

    conn.commit()
    return count


def main():
    """主函数"""
    db_path = "instance/database.db"

    print("=" * 60)
    print("批量翻译中文内容到英文")
    print("=" * 60)
    print()

    try:
        conn = sqlite3.connect(db_path)

        print("📦 翻译产品数据...")
        product_count = translate_products(conn)
        print(f"   完成 {product_count} 个产品的翻译\n")

        print("📰 翻译文章数据...")
        post_count = translate_posts(conn)
        print(f"   完成 {post_count} 篇文章的翻译\n")

        print("🎉 翻译活动数据...")
        event_count = translate_events(conn)
        print(f"   完成 {event_count} 个活动的翻译\n")

        print("📄 翻译单页数据...")
        page_count = translate_single_pages(conn)
        print(f"   完成 {page_count} 个单页的翻译\n")

        conn.close()

        print("=" * 60)
        print(f"✅ 翻译完成!")
        print(f"   - 产品: {product_count} 个")
        print(f"   - 文章: {post_count} 篇")
        print(f"   - 活动: {event_count} 个")
        print(f"   - 单页: {page_count} 个")
        print(f"   - 总计: {product_count + post_count + event_count + page_count} 条")
        print("=" * 60)
        print()
        print("⚠️  注意：这是基于词典的简单翻译，建议通过管理后台人工审核和优化！")

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
