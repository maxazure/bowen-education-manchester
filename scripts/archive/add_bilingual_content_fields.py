#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：为 Post 和 SinglePage 表添加英文字段
支持文章和单页的双语内容存储

执行方式：
    python add_bilingual_content_fields.py
"""

import sqlite3
import sys
from pathlib import Path

# 数据库路径
DB_PATH = Path(__file__).parent / "instance" / "database.db"


def check_column_exists(cursor, table_name, column_name):
    """检查字段是否已存在"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns


def add_bilingual_fields():
    """添加双语字段到 Post 和 SinglePage 表"""

    if not DB_PATH.exists():
        print(f"❌ 错误：数据库文件不存在: {DB_PATH}")
        sys.exit(1)

    print(f"📂 连接数据库: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # ============================================
        # 第一部分：为 Post 表添加英文字段
        # ============================================
        print("\n" + "="*60)
        print("📝 为 Post 表添加英文字段...")
        print("="*60)

        post_fields = [
            ("title_en", "VARCHAR(200)", "英文标题"),
            ("summary_en", "TEXT", "英文摘要"),
            ("content_html_en", "TEXT", "英文内容HTML"),
            ("content_markdown_en", "TEXT", "英文内容Markdown"),
            ("seo_title_en", "VARCHAR(200)", "英文SEO标题"),
            ("seo_description_en", "TEXT", "英文SEO描述"),
        ]

        for field_name, field_type, comment in post_fields:
            if check_column_exists(cursor, "post", field_name):
                print(f"  ⚠️  字段已存在，跳过: {field_name}")
            else:
                sql = f"ALTER TABLE post ADD COLUMN {field_name} {field_type}"
                cursor.execute(sql)
                print(f"  ✅ 添加字段: {field_name} ({comment})")

        # ============================================
        # 第二部分：为 SinglePage 表添加英文字段
        # ============================================
        print("\n" + "="*60)
        print("📄 为 SinglePage 表添加英文字段...")
        print("="*60)

        single_page_fields = [
            ("title_en", "VARCHAR(200)", "英文标题"),
            ("subtitle_en", "VARCHAR(300)", "英文副标题"),
            ("content_html_en", "TEXT", "英文内容HTML"),
            ("content_markdown_en", "TEXT", "英文内容Markdown"),
            ("seo_title_en", "VARCHAR(200)", "英文SEO标题"),
            ("seo_description_en", "TEXT", "英文SEO描述"),
        ]

        for field_name, field_type, comment in single_page_fields:
            if check_column_exists(cursor, "single_page", field_name):
                print(f"  ⚠️  字段已存在，跳过: {field_name}")
            else:
                sql = f"ALTER TABLE single_page ADD COLUMN {field_name} {field_type}"
                cursor.execute(sql)
                print(f"  ✅ 添加字段: {field_name} ({comment})")

        # 提交更改
        conn.commit()

        # ============================================
        # 第三部分：验证字段已添加
        # ============================================
        print("\n" + "="*60)
        print("🔍 验证字段已成功添加...")
        print("="*60)

        # 验证 Post 表
        cursor.execute("PRAGMA table_info(post)")
        post_columns = [row[1] for row in cursor.fetchall()]
        post_en_fields = [f for f, _, _ in post_fields]

        print(f"\n📝 Post 表字段验证 (共 {len(post_columns)} 个字段):")
        for field in post_en_fields:
            if field in post_columns:
                print(f"  ✅ {field}")
            else:
                print(f"  ❌ {field} - 缺失！")

        # 验证 SinglePage 表
        cursor.execute("PRAGMA table_info(single_page)")
        single_page_columns = [row[1] for row in cursor.fetchall()]
        single_page_en_fields = [f for f, _, _ in single_page_fields]

        print(f"\n📄 SinglePage 表字段验证 (共 {len(single_page_columns)} 个字段):")
        for field in single_page_en_fields:
            if field in single_page_columns:
                print(f"  ✅ {field}")
            else:
                print(f"  ❌ {field} - 缺失！")

        # ============================================
        # 第四部分：统计现有数据
        # ============================================
        print("\n" + "="*60)
        print("📊 数据统计...")
        print("="*60)

        cursor.execute("SELECT COUNT(*) FROM post")
        post_count = cursor.fetchone()[0]
        print(f"\n📝 Post 表: {post_count} 篇文章")
        print(f"   💡 提示: 这些文章需要添加英文内容")

        cursor.execute("SELECT COUNT(*) FROM single_page")
        page_count = cursor.fetchone()[0]
        print(f"\n📄 SinglePage 表: {page_count} 个单页")
        print(f"   💡 提示: 这些单页需要添加英文内容")

        print("\n" + "="*60)
        print("✅ 迁移完成！")
        print("="*60)
        print("\n📌 后续步骤:")
        print("   1. 更新 Post 和 SinglePage 模型定义")
        print("   2. 更新模板使用 *_en 字段")
        print("   3. 在管理后台添加英文内容")
        print()

    except Exception as e:
        conn.rollback()
        print(f"\n❌ 迁移失败: {e}")
        sys.exit(1)

    finally:
        conn.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 开始数据库迁移")
    print("="*60)
    print(f"📝 任务: 为 Post 和 SinglePage 表添加英文字段")
    print(f"🎯 目标: 支持文章和单页的双语内容存储")
    print("="*60 + "\n")

    add_bilingual_fields()
