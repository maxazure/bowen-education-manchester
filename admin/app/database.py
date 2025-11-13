"""
数据库连接配置

直接复制主项目的数据库配置，避免循环导入。
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import sys
from pathlib import Path

# 添加主项目路径到sys.path
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 从主项目导入配置
from app.config import settings as main_settings

# 创建数据库引擎
engine = create_engine(
    main_settings.database_url,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in main_settings.database_url else {}
    ),
    echo=main_settings.debug,
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建模型基类
Base = declarative_base()


def get_db():
    """
    获取数据库会话依赖

    Yields:
        数据库会话实例
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = ["Base", "engine", "SessionLocal", "get_db"]
