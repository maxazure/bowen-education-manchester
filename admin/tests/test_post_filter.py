"""
测试文章筛选功能
"""

from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from app.models.post import Post, PostCategory
from app.models.site import ColumnType, SiteColumn


def test_filter_by_column(db_session: Session):
    """测试按栏目筛选"""
    # 创建两个栏目
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

    # 在两个栏目中创建文章
    post1 = Post(
        column_id=column1.id,
        title="新闻文章",
        slug="news-post",
        content_html="<p>新闻内容</p>",
    )
    post2 = Post(
        column_id=column2.id,
        title="博客文章",
        slug="blog-post",
        content_html="<p>博客内容</p>",
    )
    db_session.add_all([post1, post2])
    db_session.commit()

    # 筛选栏目1的文章
    posts = db_session.query(Post).filter(Post.column_id == column1.id).all()
    assert len(posts) == 1
    assert posts[0].title == "新闻文章"

    # 筛选栏目2的文章
    posts = db_session.query(Post).filter(Post.column_id == column2.id).all()
    assert len(posts) == 1
    assert posts[0].title == "博客文章"


def test_filter_by_category(db_session: Session):
    """测试按分类筛选"""
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

    # 创建文章并设置分类
    post1 = Post(
        column_id=column.id,
        title="体育新闻",
        slug="sports-news",
        content_html="<p>体育内容</p>",
    )
    post1.categories.append(cat1)

    post2 = Post(
        column_id=column.id,
        title="科技新闻",
        slug="tech-news",
        content_html="<p>科技内容</p>",
    )
    post2.categories.append(cat2)

    post3 = Post(
        column_id=column.id,
        title="综合新闻",
        slug="mixed-news",
        content_html="<p>综合内容</p>",
    )
    post3.categories.extend([cat1, cat2])

    db_session.add_all([post1, post2, post3])
    db_session.commit()

    # 筛选体育分类的文章
    posts = (
        db_session.query(Post)
        .join(Post.categories)
        .filter(PostCategory.id == cat1.id)
        .all()
    )
    assert len(posts) == 2
    titles = [p.title for p in posts]
    assert "体育新闻" in titles
    assert "综合新闻" in titles


def test_filter_by_status(db_session: Session):
    """测试按状态筛选"""
    # 创建栏目
    column = SiteColumn(
        name="新闻",
        slug="news",
        column_type=ColumnType.POST,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建不同状态的文章
    post1 = Post(
        column_id=column.id,
        title="草稿文章",
        slug="draft-post",
        content_html="<p>内容</p>",
        status="draft",
    )
    post2 = Post(
        column_id=column.id,
        title="已发布文章",
        slug="published-post",
        content_html="<p>内容</p>",
        status="published",
        published_at=datetime.now(),
    )
    post3 = Post(
        column_id=column.id,
        title="下线文章",
        slug="offline-post",
        content_html="<p>内容</p>",
        status="offline",
    )
    db_session.add_all([post1, post2, post3])
    db_session.commit()

    # 筛选草稿
    drafts = db_session.query(Post).filter(Post.status == "draft").all()
    assert len(drafts) == 1
    assert drafts[0].title == "草稿文章"

    # 筛选已发布
    published = db_session.query(Post).filter(Post.status == "published").all()
    assert len(published) == 1
    assert published[0].title == "已发布文章"


def test_keyword_search(db_session: Session):
    """测试关键词搜索"""
    # 创建栏目
    column = SiteColumn(
        name="新闻",
        slug="news",
        column_type=ColumnType.POST,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建文章
    post1 = Post(
        column_id=column.id,
        title="Python 教程",
        slug="python-tutorial",
        summary="学习 Python 编程",
        content_html="<p>Python 是一门强大的语言</p>",
    )
    post2 = Post(
        column_id=column.id,
        title="JavaScript 教程",
        slug="js-tutorial",
        summary="学习 JavaScript 编程",
        content_html="<p>JavaScript 用于前端开发</p>",
    )
    post3 = Post(
        column_id=column.id,
        title="数据库设计",
        slug="database-design",
        summary="如何设计数据库",
        content_html="<p>数据库是应用的核心</p>",
    )
    db_session.add_all([post1, post2, post3])
    db_session.commit()

    # 搜索标题包含 "教程" 的文章
    keyword = "教程"
    posts = db_session.query(Post).filter(Post.title.contains(keyword)).all()
    assert len(posts) == 2
    titles = [p.title for p in posts]
    assert "Python 教程" in titles
    assert "JavaScript 教程" in titles

    # 搜索标题或摘要包含 "Python" 的文章
    keyword = "Python"
    posts = (
        db_session.query(Post)
        .filter((Post.title.contains(keyword)) | (Post.summary.contains(keyword)))
        .all()
    )
    assert len(posts) == 1
    assert posts[0].title == "Python 教程"


def test_pagination(db_session: Session):
    """测试分页"""
    # 创建栏目
    column = SiteColumn(
        name="新闻",
        slug="news",
        column_type=ColumnType.POST,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建25篇文章
    posts = []
    for i in range(1, 26):
        post = Post(
            column_id=column.id,
            title=f"文章 {i}",
            slug=f"post-{i}",
            content_html=f"<p>内容 {i}</p>",
        )
        posts.append(post)
    db_session.add_all(posts)
    db_session.commit()

    # 测试第1页（每页20条）
    page_size = 20
    page1 = db_session.query(Post).order_by(Post.id).limit(page_size).offset(0).all()
    assert len(page1) == 20

    # 测试第2页
    page2 = db_session.query(Post).order_by(Post.id).limit(page_size).offset(20).all()
    assert len(page2) == 5

    # 测试总数
    total = db_session.query(Post).count()
    assert total == 25

    # 计算总页数
    import math

    total_pages = math.ceil(total / page_size)
    assert total_pages == 2
