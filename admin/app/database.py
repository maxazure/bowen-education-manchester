"""
数据库连接配置

复用主项目的数据库连接。
"""

import sys
from pathlib import Path

# 添加主项目路径到sys.path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 从主项目导入数据库配置
from app.database import Base, SessionLocal, engine, get_db  # noqa: E402

__all__ = ["Base", "engine", "SessionLocal", "get_db"]
