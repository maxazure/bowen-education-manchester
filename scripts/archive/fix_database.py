#!/usr/bin/env python3
"""
数据库一致性修复脚本
Database Consistency Fix Script

修复内容：
1. 重复栏目名称
2. 联系信息不一致
3. 其他数据一致性问题
"""

import sqlite3
from datetime import datetime

# 数据库路径
DB_PATH = "instance/database.db"

def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def execute_query(cursor, query, params=None, fetch=True):
    """执行查询并返回结果"""
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if fetch:
        return cursor.fetchall()
    return None

def main():
    """主函数"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    fixes = []

    try:
        # ===== 1. 检查重复栏目名称 =====
        print_section("1. 检查重复栏目名称")

        # 查询所有栏目
        cursor.execute("""
            SELECT id, name, slug, parent_id
            FROM site_column
            ORDER BY name
        """)
        columns = cursor.fetchall()

        print(f"\n找到 {len(columns)} 个栏目：")
        for col in columns:
            print(f"  ID: {col[0]}, Name: {col[1]}, Slug: {col[2]}, Parent: {col[3]}")

        # 查询重复名称
        cursor.execute("""
            SELECT name, COUNT(*) as count
            FROM site_column
            GROUP BY name
            HAVING count > 1
        """)
        duplicates = cursor.fetchall()

        if duplicates:
            print(f"\n发现 {len(duplicates)} 个重复栏目名称：")
            for dup in duplicates:
                print(f"  '{dup[0]}' 出现 {dup[1]} 次")

                # 查询该名称的所有记录
                cursor.execute("""
                    SELECT id, name, slug, parent_id
                    FROM site_column
                    WHERE name = ?
                """, (dup[0],))
                same_name = cursor.fetchall()

                for record in same_name:
                    print(f"    - ID: {record[0]}, Slug: {record[2]}")
        else:
            print("\n✓ 没有发现重复的栏目名称")

        # 修复重复的"课程设置"
        print("\n修复重复的栏目名称：")

        # 查找 slug 为 school-curriculum 的记录
        cursor.execute("""
            SELECT id, name, slug
            FROM site_column
            WHERE slug = 'school-curriculum' AND name = '课程设置'
        """)
        school_curriculum = cursor.fetchone()

        # 查找 slug 为 chess-courses 的记录
        cursor.execute("""
            SELECT id, name, slug
            FROM site_column
            WHERE slug = 'chess-courses' AND name = '课程设置'
        """)
        chess_courses = cursor.fetchone()

        if school_curriculum:
            # 更新为"中文学校课程设置"
            cursor.execute("""
                UPDATE site_column
                SET name = '中文学校课程设置',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (school_curriculum[0],))
            print(f"  ✓ 更新 ID {school_curriculum[0]} (slug: school-curriculum): '课程设置' -> '中文学校课程设置'")
            fixes.append(f"重命名栏目 ID {school_curriculum[0]}: '课程设置' -> '中文学校课程设置'")

        if chess_courses:
            # 更新为"国际象棋课程设置"
            cursor.execute("""
                UPDATE site_column
                SET name = '国际象棋课程设置',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (chess_courses[0],))
            print(f"  ✓ 更新 ID {chess_courses[0]} (slug: chess-courses): '课程设置' -> '国际象棋课程设置'")
            fixes.append(f"重命名栏目 ID {chess_courses[0]}: '课程设置' -> '国际象棋课程设置'")

        # ===== 2. 检查联系信息 =====
        print_section("2. 检查联系信息")

        # 查询 site_setting 表中的联系信息
        cursor.execute("""
            SELECT id, setting_key, value_text
            FROM site_setting
            WHERE setting_key LIKE '%phone%'
               OR setting_key LIKE '%tel%'
               OR setting_key LIKE '%contact%'
               OR setting_key LIKE '%address%'
               OR setting_key LIKE '%email%'
            ORDER BY setting_key
        """)
        settings = cursor.fetchall()

        if settings:
            print(f"\n找到 {len(settings)} 条联系信息设置：")
            for setting in settings:
                print(f"  ID: {setting[0]}, Key: {setting[1]}, Value: {setting[2]}")
        else:
            print("\n在 site_setting 表中未找到联系信息")

        # 正确的联系信息（根据 README.md）
        correct_phone = "0161 969 3071"
        correct_email = "info@boweneducation.co.uk"
        correct_address = "1/F, 2A Curzon Road, Sale, Manchester M33 7DR, UK"

        # 更新电话号码
        cursor.execute("""
            SELECT id, setting_key, value_text
            FROM site_setting
            WHERE (setting_key LIKE '%phone%' OR setting_key LIKE '%tel%')
              AND value_text != ?
        """, (correct_phone,))
        wrong_phones = cursor.fetchall()

        if wrong_phones:
            print(f"\n发现 {len(wrong_phones)} 条错误的电话号码：")
            for phone in wrong_phones:
                print(f"  Key: {phone[1]}, 当前值: {phone[2]} -> 正确值: {correct_phone}")
                cursor.execute("""
                    UPDATE site_setting
                    SET value_text = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (correct_phone, phone[0]))
                fixes.append(f"更新联系电话 {phone[1]}: '{phone[2]}' -> '{correct_phone}'")
        else:
            print(f"\n✓ 电话号码正确: {correct_phone}")

        # ===== 3. 检查其他数据一致性问题 =====
        print_section("3. 检查其他数据一致性问题")

        # 3.1 检查重复的 slug
        print("\n3.1 检查重复的 slug:")
        cursor.execute("""
            SELECT slug, COUNT(*) as count
            FROM site_column
            WHERE slug IS NOT NULL AND slug != ''
            GROUP BY slug
            HAVING count > 1
        """)
        dup_slugs = cursor.fetchall()

        if dup_slugs:
            print(f"  发现 {len(dup_slugs)} 个重复的 slug：")
            for slug in dup_slugs:
                print(f"    '{slug[0]}' 出现 {slug[1]} 次")
                cursor.execute("""
                    SELECT id, name, slug
                    FROM site_column
                    WHERE slug = ?
                """, (slug[0],))
                records = cursor.fetchall()
                for rec in records:
                    print(f"      - ID: {rec[0]}, Name: {rec[1]}")
        else:
            print("  ✓ 没有重复的 slug")

        # 3.2 检查启用状态字段
        print("\n3.2 检查栏目启用状态字段:")
        cursor.execute("""
            SELECT is_enabled, COUNT(*) as count
            FROM site_column
            GROUP BY is_enabled
        """)
        statuses = cursor.fetchall()

        print(f"  栏目启用状态分布：")
        for status in statuses:
            status_name = "启用" if status[0] == 1 else ("禁用" if status[0] == 0 else "NULL")
            print(f"    {status_name}: {status[1]} 个")

        # 3.3 检查日期字段
        print("\n3.3 检查日期字段:")
        cursor.execute("""
            SELECT id, name, created_at, updated_at
            FROM site_column
            WHERE created_at IS NULL OR updated_at IS NULL
        """)
        null_dates = cursor.fetchall()

        if null_dates:
            print(f"  发现 {len(null_dates)} 个栏目日期字段为空：")
            for record in null_dates:
                print(f"    ID: {record[0]}, Name: {record[1]}, Created: {record[2]}, Updated: {record[3]}")
        else:
            print("  ✓ 所有栏目日期字段正常")

        # 3.4 检查产品表中的栏目引用
        print("\n3.4 检查产品表中的栏目引用:")
        cursor.execute("""
            SELECT p.id, p.name, p.column_id, c.name as column_name
            FROM product p
            LEFT JOIN site_column c ON p.column_id = c.id
            WHERE p.column_id IS NOT NULL
            ORDER BY p.column_id
        """)
        products = cursor.fetchall()

        if products:
            print(f"  找到 {len(products)} 个产品/课程：")
            for prod in products:
                col_name = prod[3] if prod[3] else '未找到栏目'
                print(f"    产品: {prod[1]}, 栏目ID: {prod[2]}, 栏目名: {col_name}")

                # 检查是否有产品引用了不存在的栏目
                if not prod[3]:
                    print(f"      ⚠️ 警告: 产品 ID {prod[0]} 引用了不存在的栏目 ID {prod[2]}")
        else:
            print("  未找到产品记录")

        # 3.5 检查文章表中的栏目引用
        print("\n3.5 检查文章表中的栏目引用:")
        cursor.execute("""
            SELECT p.id, p.title, p.column_id, c.name as column_name
            FROM post p
            LEFT JOIN site_column c ON p.column_id = c.id
            WHERE p.column_id IS NOT NULL
            ORDER BY p.column_id
        """)
        posts = cursor.fetchall()

        if posts:
            print(f"  找到 {len(posts)} 篇文章：")
            for post in posts:
                col_name = post[3] if post[3] else '未找到栏目'
                print(f"    文章: {post[1]}, 栏目ID: {post[2]}, 栏目名: {col_name}")

                # 检查是否有文章引用了不存在的栏目
                if not post[3]:
                    print(f"      ⚠️ 警告: 文章 ID {post[0]} 引用了不存在的栏目 ID {post[2]}")
        else:
            print("  未找到文章记录")

        # ===== 提交更改 =====
        print_section("提交更改")

        if fixes:
            conn.commit()
            print(f"\n✓ 成功提交 {len(fixes)} 项修复")
        else:
            print("\n未发现需要修复的问题")

        # ===== 验证修复 =====
        print_section("验证修复结果")

        # 验证栏目名称
        print("\n验证栏目名称:")
        cursor.execute("""
            SELECT id, name, slug
            FROM site_column
            WHERE slug IN ('school-curriculum', 'chess-courses')
            ORDER BY slug
        """)
        verified = cursor.fetchall()

        for col in verified:
            print(f"  ✓ ID: {col[0]}, Name: {col[1]}, Slug: {col[2]}")

        # 验证联系信息
        print("\n验证联系信息:")
        cursor.execute("""
            SELECT setting_key, value_text
            FROM site_setting
            WHERE setting_key LIKE '%phone%' OR setting_key LIKE '%tel%'
            ORDER BY setting_key
        """)
        verified_phones = cursor.fetchall()

        for phone in verified_phones:
            print(f"  ✓ {phone[0]}: {phone[1]}")

        # ===== 修复总结 =====
        print_section("修复总结")

        if fixes:
            print(f"\n共完成 {len(fixes)} 项修复：\n")
            for i, fix in enumerate(fixes, 1):
                print(f"{i}. {fix}")
        else:
            print("\n数据库数据一致性良好，未发现需要修复的问题。")

        print("\n" + "=" * 60)
        print(" 修复完成！")
        print("=" * 60 + "\n")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
