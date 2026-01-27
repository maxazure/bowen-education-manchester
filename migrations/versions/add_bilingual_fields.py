"""添加双语字段迁移脚本

此脚本为 SiteColumn 添加 content_html 和 content_html_en 字段
为 Gallery 添加 title_en 和 description_en 字段

执行方式:
    cd /path/to/project
    . venv/bin/activate
    python migrations/versions/add_bilingual_fields.py
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine, text

# 读取数据库配置
from app.config import settings

# 创建数据库引擎
DATABASE_URL = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'instance', 'database.db')}"
engine = create_engine(DATABASE_URL)

def migrate():
    """执行迁移"""

    print("开始迁移数据库...")

    # 为 SiteColumn 添加 content_html 和 content_html_en 字段
    print("\n1. 为 SiteColumn 添加 content_html 字段...")

    try:
        with engine.connect() as conn:
            # 检查字段是否已存在
            result = conn.execute(text("PRAGMA table_info(site_column)"))
            columns = [row[1] for row in result.fetchall()]

            if 'content_html' not in columns:
                conn.execute(text("ALTER TABLE site_column ADD COLUMN content_html TEXT"))
                print("  - content_html 字段添加成功")
            else:
                print("  - content_html 字段已存在")

            if 'content_html_en' not in columns:
                conn.execute(text("ALTER TABLE site_column ADD COLUMN content_html_en TEXT"))
                print("  - content_html_en 字段添加成功")
            else:
                print("  - content_html_en 字段已存在")

            conn.commit()
    except Exception as e:
        print(f"  - SiteColumn 迁移出错: {e}")

    # 为 Gallery 添加 title_en 和 description_en 字段
    print("\n2. 为 Gallery 添加双语字段...")

    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(gallery)"))
            columns = [row[1] for row in result.fetchall()]

            if 'title_en' not in columns:
                conn.execute(text("ALTER TABLE gallery ADD COLUMN title_en VARCHAR(200)"))
                print("  - title_en 字段添加成功")
            else:
                print("  - title_en 字段已存在")

            if 'description_en' not in columns:
                conn.execute(text("ALTER TABLE gallery ADD COLUMN description_en TEXT"))
                print("  - description_en 字段添加成功")
            else:
                print("  - description_en 字段已存在")

            conn.commit()
    except Exception as e:
        print(f"  - Gallery 迁移出错: {e}")

    print("\n迁移完成！")

if __name__ == "__main__":
    migrate()
