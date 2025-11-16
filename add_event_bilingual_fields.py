"""
数据库迁移脚本: 为 Event 添加英文字段

执行命令:
python add_event_bilingual_fields.py

作者: maxazure
日期: 2025-11-16
"""

import sqlite3
import sys
from pathlib import Path

# 数据库文件路径
DB_PATH = "instance/database.db"


def add_bilingual_fields():
    """为 Event 表添加英文字段"""

    # 检查数据库文件是否存在
    if not Path(DB_PATH).exists():
        print(f"❌ 错误: 数据库文件不存在: {DB_PATH}")
        sys.exit(1)

    try:
        # 连接数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("🚀 开始为 Event 表添加英文字段...")
        print("-" * 60)

        # ===== Event 表 =====
        print("\n📦 处理 Event 表...")

        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(event)")
        existing_columns = [row[1] for row in cursor.fetchall()]

        event_fields = [
            ("title_en", "VARCHAR(200)", "活动英文标题"),
            ("description_en", "TEXT", "活动英文描述"),
            ("summary_en", "TEXT", "活动英文简介"),
            ("venue_name_en", "VARCHAR(200)", "场地英文名称"),
            ("seo_title_en", "VARCHAR(200)", "英文SEO标题"),
            ("seo_description_en", "TEXT", "英文SEO描述"),
        ]

        for field_name, field_type, comment in event_fields:
            if field_name in existing_columns:
                print(f"  ⚠️  字段 {field_name} 已存在,跳过")
            else:
                sql = f"ALTER TABLE event ADD COLUMN {field_name} {field_type}"
                cursor.execute(sql)
                print(f"  ✅ 添加字段: {field_name} ({comment})")

        # 提交事务
        conn.commit()

        print("\n" + "-" * 60)
        print("✅ 数据库迁移成功完成!")

        # ===== 验证字段 =====
        print("\n🔍 验证新增字段...")

        # 验证 Event
        cursor.execute("PRAGMA table_info(event)")
        event_columns = [row[1] for row in cursor.fetchall()]
        print(f"\n📊 Event 表字段数: {len(event_columns)}")
        en_fields = [f for f in event_columns if f.endswith('_en')]
        print(f"   英文字段数量: {len(en_fields)}")
        print(f"   英文字段列表: {', '.join(en_fields)}")

        # 统计数据
        cursor.execute("SELECT COUNT(*) FROM event")
        event_count = cursor.fetchone()[0]
        print(f"\n📈 Event 记录数: {event_count}")

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
    print("Event 双语字段迁移脚本")
    print("=" * 60)

    add_bilingual_fields()
