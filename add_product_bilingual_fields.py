"""
数据库迁移脚本: 为 Product 和 ProductCategory 添加英文字段

执行命令:
python add_product_bilingual_fields.py

作者: maxazure
日期: 2025-11-16
"""

import sqlite3
import sys
from pathlib import Path

# 数据库文件路径
DB_PATH = "instance/database.db"


def add_bilingual_fields():
    """为 Product 和 ProductCategory 表添加英文字段"""

    # 检查数据库文件是否存在
    if not Path(DB_PATH).exists():
        print(f"❌ 错误: 数据库文件不存在: {DB_PATH}")
        sys.exit(1)

    try:
        # 连接数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("🚀 开始为 Product 和 ProductCategory 表添加英文字段...")
        print("-" * 60)

        # ===== ProductCategory 表 =====
        print("\n📦 处理 ProductCategory 表...")

        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(product_category)")
        existing_columns = [row[1] for row in cursor.fetchall()]

        category_fields = [
            ("name_en", "VARCHAR(100)", "分类英文名称"),
        ]

        for field_name, field_type, comment in category_fields:
            if field_name in existing_columns:
                print(f"  ⚠️  字段 {field_name} 已存在,跳过")
            else:
                sql = f"ALTER TABLE product_category ADD COLUMN {field_name} {field_type}"
                cursor.execute(sql)
                print(f"  ✅ 添加字段: {field_name} ({comment})")

        # ===== Product 表 =====
        print("\n📦 处理 Product 表...")

        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(product)")
        existing_columns = [row[1] for row in cursor.fetchall()]

        product_fields = [
            ("name_en", "VARCHAR(200)", "产品英文名称"),
            ("summary_en", "TEXT", "产品英文简述"),
            ("description_html_en", "TEXT", "英文详细说明HTML"),
            ("price_text_en", "VARCHAR(100)", "英文价格文本"),
            ("seo_title_en", "VARCHAR(200)", "英文SEO标题"),
            ("seo_description_en", "TEXT", "英文SEO描述"),
        ]

        for field_name, field_type, comment in product_fields:
            if field_name in existing_columns:
                print(f"  ⚠️  字段 {field_name} 已存在,跳过")
            else:
                sql = f"ALTER TABLE product ADD COLUMN {field_name} {field_type}"
                cursor.execute(sql)
                print(f"  ✅ 添加字段: {field_name} ({comment})")

        # 提交事务
        conn.commit()

        print("\n" + "-" * 60)
        print("✅ 数据库迁移成功完成!")

        # ===== 验证字段 =====
        print("\n🔍 验证新增字段...")

        # 验证 ProductCategory
        cursor.execute("PRAGMA table_info(product_category)")
        category_columns = [row[1] for row in cursor.fetchall()]
        print(f"\n📊 ProductCategory 表字段数: {len(category_columns)}")
        print(f"   包含 name_en: {'✅' if 'name_en' in category_columns else '❌'}")

        # 验证 Product
        cursor.execute("PRAGMA table_info(product)")
        product_columns = [row[1] for row in cursor.fetchall()]
        print(f"\n📊 Product 表字段数: {len(product_columns)}")
        en_fields = [f for f in product_columns if f.endswith('_en')]
        print(f"   英文字段数量: {len(en_fields)}")
        print(f"   英文字段列表: {', '.join(en_fields)}")

        # 统计数据
        cursor.execute("SELECT COUNT(*) FROM product_category")
        category_count = cursor.fetchone()[0]
        print(f"\n📈 ProductCategory 记录数: {category_count}")

        cursor.execute("SELECT COUNT(*) FROM product")
        product_count = cursor.fetchone()[0]
        print(f"📈 Product 记录数: {product_count}")

        print("\n" + "=" * 60)
        print("✅ 所有操作完成!")
        print("=" * 60)

    except sqlite3.Error as e:
        print(f"\n❌ 数据库错误: {e}")
        conn.rollback()
        sys.exit(1)

    finally:
        # 关闭连接
        if conn:
            conn.close()
            print("\n🔒 数据库连接已关闭")


if __name__ == "__main__":
    print("=" * 60)
    print("Product & ProductCategory 双语字段迁移脚本")
    print("=" * 60)

    add_bilingual_fields()
