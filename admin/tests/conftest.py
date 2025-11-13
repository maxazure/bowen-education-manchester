"""
管理后台测试配置
"""
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 设置测试环境标志
os.environ["TESTING"] = "1"

# 添加主项目路径到sys.path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.database import Base, get_db  # noqa: E402
from admin.app.main import app  # noqa: E402


# 创建测试数据库引擎
TEST_DATABASE_URL = "sqlite:///./test_admin.db"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库"""
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """创建数据库会话"""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db
    )
    connection = test_db.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """创建测试客户端"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # TestClient 会自动管理 cookies，包括 session cookies
    test_client = TestClient(app)

    yield test_client

    app.dependency_overrides.clear()
