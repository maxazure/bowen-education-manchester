#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化英文导航栏目名称
使其更简洁，符合英文网站排版习惯
"""

import sqlite3


def optimize_navigation():
    """优化导航栏目的英文名称"""

    # 栏目名称优化映射（基于 slug 匹配）
    optimized_names = {
        'about': 'About',                    # 关于博文: About Bowen → About
        'school': 'School',                  # 中文学校: Chinese School → School
        'tuition': 'Tutoring',               # 补习中心: Tuition Centre → Tutoring
        'chess': 'Chess',                    # 国际象棋俱乐部: Chess Club → Chess (保持)
        'badminton': 'Badminton',            # 羽毛球俱乐部: Badminton Club → Badminton
        'programmes': 'Programs',            # 政府项目: Government Programmes → Programs
        'events': 'Events',                  # 博文活动: Events & Activities → Events
        'contact': 'Contact',                # 联系我们: Contact Us → Contact (保持)
        'news': 'News',                      # 博文新闻: News → News (保持)
        'about-company': 'Our Story',        # 博文集团: About Us → Our Story
        'chess-about': 'About',              # 俱乐部简介: About Club → About
        'chess-courses': 'Courses',          # 国际象棋课程设置: Chess Courses → Courses
        'chess-resources': 'Resources',      # 学习资源: Learning Resources → Resources
        'chess-news': 'Highlights',          # 新闻与精彩回顾: News & Highlights → Highlights
    }

    db_path = "instance/database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 70)
    print("优化导航栏目英文名称")
    print("=" * 70)
    print()

    # 获取所有启用的导航栏目
    cursor.execute("""
        SELECT id, name, name_en, slug
        FROM site_column
        WHERE is_enabled = 1
        ORDER BY sort_order
    """)

    columns = cursor.fetchall()
    updated_count = 0

    for col_id, name_zh, name_en_old, slug in columns:
        if slug in optimized_names:
            name_en_new = optimized_names[slug]

            if name_en_new != name_en_old:
                cursor.execute("""
                    UPDATE site_column
                    SET name_en = ?
                    WHERE id = ?
                """, (name_en_new, col_id))

                updated_count += 1
                print(f"✓ {name_zh} ({slug})")
                print(f"  {name_en_old} → {name_en_new}")
                print()

    conn.commit()
    conn.close()

    print("=" * 70)
    print(f"✅ 已优化 {updated_count} 个导航栏目名称")
    print("=" * 70)
    print()
    print("优化原则:")
    print("1. 简洁明了 - 单个词或最多两个词")
    print("2. 符合英文习惯 - 使用常见的导航术语")
    print("3. 保持语义清晰 - 用户能够快速理解")
    print("4. 适合窄屏显示 - 移动端友好")


if __name__ == "__main__":
    optimize_navigation()
