"""
管理后台测试配置
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from admin.app.database import Base
from admin.app.main import app


@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库"""
    engine = create_engine("sqlite:///./test_admin.db")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """创建数据库会话"""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db
    )
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def client():
    """创建测试客户端"""
    return TestClient(app)
