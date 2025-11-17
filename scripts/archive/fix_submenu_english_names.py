#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正和优化子菜单的英文名称
"""

import sqlite3


def fix_submenu_names():
    """修正子菜单的英文名称"""

    # 子菜单英文名称修正和优化
    submenu_updates = {
        # Badminton 子菜单
        'badminton-events': 'Events',           # 赛事活动
        'badminton-schedule': 'Schedule',       # 训练时间表
        'badminton-gallery': 'Gallery',         # 精彩瞬间

        # Events 子菜单
        'events-henan': 'Henan Partnership',    # 河南大学合作

        # About 子菜单优化
        'about-company': 'Our Story',           # 博文集团 (保持)

        # School 子菜单优化
        'school-curriculum': 'Curriculum',      # 中文学校课程设置: Chinese School Curriculum → Curriculum
        'school-term-dates': 'Term Dates',      # 学期日期 (保持)
        'school-pta': 'PTA',                    # PTA家长教师协会: Parent-Teacher Association → PTA

        # Chess 子菜单 (已优化，保持)
        'chess-about': 'About',
        'chess-courses': 'Courses',
        'chess-events': 'Competitions',         # 活动与赛事: Events & Competitions → Competitions
        'chess-resources': 'Resources',
        'chess-news': 'Highlights',

        # Programs 子菜单优化
        'programmes-haf': 'HAF Program',        # HAF项目: HAF Programme → HAF Program
        'programmes-parks': 'Park Activities',  # 公园活动 (保持)
    }

    db_path = "instance/database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 70)
    print("修正和优化子菜单英文名称")
    print("=" * 70)
    print()

    updated_count = 0

    for slug, name_en_new in submenu_updates.items():
        cursor.execute("""
            SELECT id, name, name_en
            FROM site_column
            WHERE slug = ?
        """, (slug,))

        result = cursor.fetchone()
        if result:
            col_id, name_zh, name_en_old = result

            if name_en_new != name_en_old:
                cursor.execute("""
                    UPDATE site_column
                    SET name_en = ?
                    WHERE id = ?
                """, (name_en_new, col_id))

                updated_count += 1
                print(f"✓ {name_zh} ({slug})")
                if name_en_old:
                    print(f"  {name_en_old} → {name_en_new}")
                else:
                    print(f"  (空) → {name_en_new}")
                print()

    conn.commit()
    conn.close()

    print("=" * 70)
    print(f"✅ 已更新 {updated_count} 个子菜单名称")
    print("=" * 70)
    print()
    print("优化原则:")
    print("1. 单词简洁 - 1-2个词最佳")
    print("2. 上下文清晰 - 结合父菜单理解")
    print("3. 统一风格 - 同类菜单命名一致")


if __name__ == "__main__":
    fix_submenu_names()
