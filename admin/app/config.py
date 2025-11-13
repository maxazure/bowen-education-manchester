"""
管理后台配置
"""

import os
from pathlib import Path

# 基础路径
ADMIN_DIR = Path(__file__).parent.parent
PROJECT_ROOT = ADMIN_DIR.parent

# 数据库配置（使用主项目的数据库）
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_ROOT}/app.db")

# Session 配置
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
SESSION_COOKIE_NAME = "admin_session"
SESSION_MAX_AGE = 86400  # 24小时

# 上传配置
UPLOAD_DIR = ADMIN_DIR / "uploads"
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

# 分页配置
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
