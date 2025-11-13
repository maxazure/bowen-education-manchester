"""
测试文章发布功能
"""

from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.site import ColumnType, SiteColumn


def test_publish(db_session: Session):
    """测试发布文章"""
    # 创建栏目和草稿文章
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
        title="待发布文章",
        slug="to-publish",
        content_html="<p>内容</p>",
        status="draft",
    )
    db_session.add(post)
    db_session.commit()

    # 发布文章
    post.status = "published"
    post.published_at = datetime.now()
    db_session.commit()

    # 验证
    db_session.refresh(post)
    assert post.status == "published"
    assert post.published_at is not None
    assert isinstance(post.published_at, datetime)


def test_unpublish(db_session: Session):
    """测试取消发布"""
    # 创建栏目和已发布文章
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
        title="已发布文章",
        slug="published-post",
        content_html="<p>内容</p>",
        status="published",
        published_at=datetime.now(),
    )
    db_session.add(post)
    db_session.commit()

    # 取消发布
    post.status = "draft"
    db_session.commit()

    # 验证
    db_session.refresh(post)
    assert post.status == "draft"
    # published_at 保留，不清空


def test_recommend(db_session: Session):
    """测试设置推荐"""
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
        title="普通文章",
        slug="normal-post",
        content_html="<p>内容</p>",
        is_recommended=False,
    )
    db_session.add(post)
    db_session.commit()

    # 设置为推荐
    post.is_recommended = True
    db_session.commit()

    # 验证
    db_session.refresh(post)
    assert post.is_recommended is True

    # 取消推荐
    post.is_recommended = False
    db_session.commit()

    db_session.refresh(post)
    assert post.is_recommended is False


def test_pin(db_session: Session):
    """测试设置置顶"""
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
        title="普通文章",
        slug="normal-post",
        content_html="<p>内容</p>",
        is_pinned=False,
    )
    db_session.add(post)
    db_session.commit()

    # 设置为置顶
    post.is_pinned = True
    db_session.commit()

    # 验证
    db_session.refresh(post)
    assert post.is_pinned is True

    # 取消置顶
    post.is_pinned = False
    db_session.commit()

    db_session.refresh(post)
    assert post.is_pinned is False

    # 测试置顶文章排序
    post1 = Post(
        column_id=column.id,
        title="普通文章1",
        slug="normal-1",
        content_html="<p>内容</p>",
        is_pinned=False,
    )
    post2 = Post(
        column_id=column.id,
        title="置顶文章",
        slug="pinned",
        content_html="<p>内容</p>",
        is_pinned=True,
    )
    post3 = Post(
        column_id=column.id,
        title="普通文章2",
        slug="normal-2",
        content_html="<p>内容</p>",
        is_pinned=False,
    )
    db_session.add_all([post1, post2, post3])
    db_session.commit()

    # 查询所有文章，置顶的应该在前面
    posts = db_session.query(Post).order_by(Post.is_pinned.desc(), Post.id.desc()).all()

    # 验证置顶文章在最前面
    pinned_posts = [p for p in posts if p.is_pinned]
    assert len(pinned_posts) >= 1
    assert posts[0].is_pinned or posts[1].is_pinned  # 前两个中至少有一个是置顶的
