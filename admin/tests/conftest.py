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


@pytest.fixture(scope="function")
def test_media_file(db_session):
    """创建测试媒体文件"""
    from app.models.media import MediaFile

    media = MediaFile(
        filename_original="test_image.jpg",
        path_original="/uploads/test_image.jpg",
        mime_type="image/jpeg",
        size_bytes=1024 * 100,  # 100KB
        width=800,
        height=600,
    )
    db_session.add(media)
    db_session.commit()
    db_session.refresh(media)

    yield media

    db_session.delete(media)
    db_session.commit()


@pytest.fixture(scope="function")
def test_media_files(db_session):
    """创建多个测试媒体文件"""
    from app.models.media import MediaFile

    media_files = []
    for i in range(5):
        media = MediaFile(
            filename_original=f"test_image_{i+1}.jpg",
            path_original=f"/uploads/test_image_{i+1}.jpg",
            mime_type="image/jpeg",
            size_bytes=1024 * 100,  # 100KB
            width=800,
            height=600,
        )
        db_session.add(media)
        media_files.append(media)

    db_session.commit()
    for media in media_files:
        db_session.refresh(media)

    yield media_files

    for media in media_files:
        db_session.delete(media)
    db_session.commit()


@pytest.fixture(scope="function")
def test_gallery(db_session):
    """创建测试相册"""
    from app.models.gallery import Gallery

    gallery = Gallery(
        title="测试相册",
        slug="test-gallery",
        description="这是一个测试相册",
        category="测试分类",
        is_public=True,
        sort_order=0,
    )
    db_session.add(gallery)
    db_session.commit()
    db_session.refresh(gallery)

    yield gallery

    db_session.delete(gallery)
    db_session.commit()
