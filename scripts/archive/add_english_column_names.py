#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add English column names to site_column table
为 site_column 表添加英文栏目名称
"""

import sqlite3

# 栏目中英文对照表
COLUMN_TRANSLATIONS = {
    "首页": "Home",
    "博文集团": "About Us",
    "关于博文": "About Bowen",
    "中文学校": "Chinese School",
    "补习中心": "Tuition Centre",
    "国际象棋俱乐部": "Chess Club",
    "羽毛球俱乐部": "Badminton Club",
    "政府项目": "Government Programmes",
    "博文活动": "Events & Activities",
    "博文新闻": "News",
    "联系我们": "Contact Us",
    "中文学校课程设置": "Chinese School Curriculum",
    "学期日期": "Term Dates",
    "家长教师协会": "Parent-Teacher Association",
    "学校特色": "School Features",
    "国际象棋课程设置": "Chess Courses",
    "俱乐部简介": "About Club",
    "学习资源": "Learning Resources",
    "新闻与精彩回顾": "News & Highlights",
    "补习课程": "Tuition Courses",
    "师资力量": "Our Teachers",
    "成功案例": "Success Stories",
    "HAF项目": "HAF Programme",
    "公园活动": "Park Activities",
    "学校合作": "School Partnerships",
    "羽毛球课程": "Badminton Courses",
    "教练介绍": "Coaches",
    "比赛活动": "Competitions & Events",
    "关于我们": "About Us",
}

def add_english_names():
    """Add English names column and populate it"""
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    try:
        # 1. 检查列是否已存在
        cursor.execute("PRAGMA table_info(site_column)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'name_en' not in columns:
            print("添加 name_en 列...")
            cursor.execute("ALTER TABLE site_column ADD COLUMN name_en VARCHAR(100)")
            conn.commit()
            print("✓ name_en 列添加成功")
        else:
            print("name_en 列已存在，跳过添加")

        # 2. 更新英文名称
        print("\n更新栏目英文名称...")
        cursor.execute("SELECT id, name FROM site_column")
        columns_data = cursor.fetchall()

        updated_count = 0
        for col_id, name_zh in columns_data:
            name_en = COLUMN_TRANSLATIONS.get(name_zh, name_zh)
            cursor.execute(
                "UPDATE site_column SET name_en = ? WHERE id = ?",
                (name_en, col_id)
            )
            print(f"  {col_id}: {name_zh} → {name_en}")
            updated_count += 1

        conn.commit()
        print(f"\n✓ 成功更新 {updated_count} 个栏目的英文名称")

        # 3. 验证结果
        print("\n验证结果:")
        cursor.execute("SELECT id, name, name_en, slug FROM site_column WHERE show_in_nav = 1 ORDER BY sort_order LIMIT 10")
        results = cursor.fetchall()
        print("\n导航栏目（前10个）:")
        print(f"{'ID':<5} {'中文名':<20} {'英文名':<25} Slug")
        print("-" * 80)
        for row in results:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<25} {row[3]}")

    except Exception as e:
        print(f"❌ 错误: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 80)
    print("添加英文栏目名称")
    print("=" * 80)
    add_english_names()
    print("\n" + "=" * 80)
    print("完成！")
    print("=" * 80)
