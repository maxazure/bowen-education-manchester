"""
测试文章 CRUD 功能
"""

from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from app.models.media import MediaFile
from app.models.post import Post, PostCategory, PostCategoryLink
from app.models.site import ColumnType, SiteColumn


def test_create_post(db_session: Session):
    """测试创建文章"""
    # 创建测试数据
    column = SiteColumn(
        name="新闻",
        slug="news",
        column_type=ColumnType.POST,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建文章
    post = Post(
        column_id=column.id,
        title="测试文章",
        slug="test-post",
        summary="这是一篇测试文章",
        content_markdown="# 标题\n\n这是内容",
        content_html="<h1>标题</h1><p>这是内容</p>",
        status="draft",
    )
    db_session.add(post)
    db_session.commit()

    # 验证
    assert post.id is not None
    assert post.title == "测试文章"
    assert post.slug == "test-post"
    assert post.content_markdown == "# 标题\n\n这是内容"
    assert post.status == "draft"
    assert post.is_recommended is False
    assert post.is_pinned is False


def test_set_column(db_session: Session):
    """测试设置栏目"""
    # 创建栏目
    column1 = SiteColumn(
        name="新闻",
        slug="news",
        column_type=ColumnType.POST,
        sort_order=1,
    )
    column2 = SiteColumn(
        name="博客",
        slug="blog",
        column_type=ColumnType.POST,
        sort_order=2,
    )
    db_session.add_all([column1, column2])
    db_session.commit()

    # 创建文章并设置栏目
    post = Post(
        column_id=column1.id,
        title="新闻文章",
        slug="news-post",
        content_html="<p>内容</p>",
    )
    db_session.add(post)
    db_session.commit()

    # 验证栏目关联
    assert post.column.name == "新闻"

    # 修改栏目
    post.column_id = column2.id
    db_session.commit()

    db_session.refresh(post)
    assert post.column.name == "博客"


def test_set_categories(db_session: Session):
    """测试设置分类（多选）"""
    # 创建栏目和分类
    column = SiteColumn(
        name="新闻",
        slug="news",
        column_type=ColumnType.POST,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    cat1 = PostCategory(
        column_id=column.id,
        name="体育",
        slug="sports",
    )
    cat2 = PostCategory(
        column_id=column.id,
        name="科技",
        slug="tech",
    )
    db_session.add_all([cat1, cat2])
    db_session.commit()

    # 创建文章
    post = Post(
        column_id=column.id,
        title="测试文章",
        slug="test-post",
        content_html="<p>内容</p>",
    )
    db_session.add(post)
    db_session.commit()

    # 设置分类（多对多关系）
    post.categories.append(cat1)
    post.categories.append(cat2)
    db_session.commit()

    # 验证
    db_session.refresh(post)
    assert len(post.categories) == 2
    category_names = [c.name for c in post.categories]
    assert "体育" in category_names
    assert "科技" in category_names


def test_set_cover(db_session: Session):
    """测试设置封面图"""
    # 创建栏目
    column = SiteColumn(
        name="新闻",
        slug="news",
        column_type=ColumnType.POST,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建媒体文件
    media = MediaFile(
        filename_original="cover.jpg",
        path_original="/uploads/2024/01/cover.jpg",
        mime_type="image/jpeg",
        size_bytes=102400,
    )
    db_session.add(media)
    db_session.commit()

    # 创建文章并设置封面
    post = Post(
        column_id=column.id,
        title="测试文章",
        slug="test-post",
        content_html="<p>内容</p>",
        cover_media_id=media.id,
    )
    db_session.add(post)
    db_session.commit()

    # 验证
    db_session.refresh(post)
    assert post.cover_media_id == media.id
    assert post.cover_media.filename_original == "cover.jpg"


def test_update_post(db_session: Session):
    """测试更新文章"""
    # 创建栏目和文章
    column = SiteColumn(
        name="新闻",
        slug="news",
        column_type=ColumnType.POST,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    post = Post(
        column_id=column.id,
        title="原标题",
        slug="original-title",
        summary="原摘要",
        content_markdown="# 原内容",
        content_html="<h1>原内容</h1>",
        status="draft",
    )
    db_session.add(post)
    db_session.commit()

    # 更新文章
    post.title = "新标题"
    post.slug = "new-title"
    post.summary = "新摘要"
    post.content_markdown = "# 新内容"
    post.content_html = "<h1>新内容</h1>"
    post.is_recommended = True
    db_session.commit()

    # 验证
    db_session.refresh(post)
    assert post.title == "新标题"
    assert post.slug == "new-title"
    assert post.summary == "新摘要"
    assert post.content_markdown == "# 新内容"
    assert post.is_recommended is True


def test_delete_post(db_session: Session):
    """测试删除文章"""
    # 创建栏目和文章
    column = SiteColumn(
        name="新闻",
        slug="news",
        column_type=ColumnType.POST,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    post = Post(
        column_id=column.id,
        title="待删除文章",
        slug="to-delete",
        content_html="<p>内容</p>",
    )
    db_session.add(post)
    db_session.commit()

    post_id = post.id

    # 删除文章
    db_session.delete(post)
    db_session.commit()

    # 验证
    deleted_post = db_session.query(Post).filter(Post.id == post_id).first()
    assert deleted_post is None
