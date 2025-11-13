#!/usr/bin/env python
"""
初始化管理员账号

使用方法: python scripts/init_admin.py
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.database import SessionLocal
from app.models.admin_user import AdminUser


def init_admin():
    """创建初始管理员账号"""
    db = SessionLocal()

    try:
        # 检查是否已有管理员
        existing = db.query(AdminUser).filter_by(username="admin").first()
        if existing:
            print("❌ 管理员账号已存在")
            print(f"   用户名: {existing.username}")
            print(f"   邮箱: {existing.email}")
            return

        # 创建初始管理员
        admin = AdminUser(
            username="admin",
            email="admin@boweneducation.org"
        )
        admin.set_password("admin123")

        db.add(admin)
        db.commit()

        print("✅ 初始管理员账号创建成功")
        print("")
        print("   用户名: admin")
        print("   密码: admin123")
        print("   邮箱: admin@boweneducation.org")
        print("")
        print("⚠️  请在首次登录后立即修改密码！")

    except Exception as e:
        print(f"❌ 创建失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_admin()
