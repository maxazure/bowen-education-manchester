"""
测试单页 CRUD 功能

测试用例:
1. 创建单页
2. 保存草稿
3. 发布单页
4. 更新单页
5. 删除单页
"""

from datetime import datetime

import pytest

from app.models.site import ColumnType, SinglePage, SiteColumn


class TestSinglePageCreate:
    """测试单页创建功能"""

    def test_create_page(self, db_session):
        """测试创建单页"""
        # 首先创建一个栏目
        column = SiteColumn(
            name="关于我们",
            slug="about",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
            show_in_nav=True,
            sort_order=0,
        )
        db_session.add(column)
        db_session.commit()
        db_session.refresh(column)

        # 创建单页
        page = SinglePage(
            column_id=column.id,
            title="关于我们",
            slug="about-us",
            subtitle="了解我们的团队",
            content_markdown="# 欢迎\n\n这是我们的团队介绍。",
            content_html="<h1>欢迎</h1><p>这是我们的团队介绍。</p>",
            status="draft",
            seo_title="关于我们 - 公司简介",
            seo_description="了解我们的历史和团队",
            seo_keywords="关于我们,团队,历史",
        )
        db_session.add(page)
        db_session.commit()
        db_session.refresh(page)

        # 验证创建成功
        assert page.id is not None
        assert page.title == "关于我们"
        assert page.slug == "about-us"
        assert page.subtitle == "了解我们的团队"
        assert page.content_markdown == "# 欢迎\n\n这是我们的团队介绍。"
        assert page.content_html == "<h1>欢迎</h1><p>这是我们的团队介绍。</p>"
        assert page.status == "draft"
        assert page.published_at is None

    def test_save_draft(self, db_session):
        """测试保存草稿"""
        # 创建栏目
        column = SiteColumn(
            name="服务",
            slug="services",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
            show_in_nav=True,
            sort_order=1,
        )
        db_session.add(column)
        db_session.commit()

        # 创建草稿单页
        page = SinglePage(
            column_id=column.id,
            title="我们的服务",
            slug="our-services",
            content_markdown="## 服务列表\n\n- 服务 1\n- 服务 2",
            content_html="<h2>服务列表</h2><ul><li>服务 1</li><li>服务 2</li></ul>",
            status="draft",
        )
        db_session.add(page)
        db_session.commit()
        db_session.refresh(page)

        # 验证草稿状态
        assert page.status == "draft"
        assert page.published_at is None

    def test_publish_page(self, db_session):
        """测试发布单页"""
        # 创建栏目
        column = SiteColumn(
            name="联系我们",
            slug="contact",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
            show_in_nav=True,
            sort_order=2,
        )
        db_session.add(column)
        db_session.commit()

        # 创建并发布单页
        page = SinglePage(
            column_id=column.id,
            title="联系我们",
            slug="contact-us",
            content_markdown="## 联系方式\n\n请通过以下方式联系我们。",
            content_html="<h2>联系方式</h2><p>请通过以下方式联系我们。</p>",
            status="published",
            published_at=datetime.now(),
        )
        db_session.add(page)
        db_session.commit()
        db_session.refresh(page)

        # 验证发布状态
        assert page.status == "published"
        assert page.published_at is not None


class TestSinglePageUpdate:
    """测试单页更新功能"""

    def test_update_page(self, db_session):
        """测试更新单页"""
        # 创建栏目和单页
        column = SiteColumn(
            name="测试栏目",
            slug="test",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
            show_in_nav=True,
            sort_order=0,
        )
        db_session.add(column)
        db_session.commit()

        page = SinglePage(
            column_id=column.id,
            title="原标题",
            slug="original-slug",
            content_markdown="原内容",
            content_html="<p>原内容</p>",
            status="draft",
        )
        db_session.add(page)
        db_session.commit()
        db_session.refresh(page)

        # 更新单页
        page.title = "新标题"
        page.content_markdown = "# 新内容\n\n更新后的内容"
        page.content_html = "<h1>新内容</h1><p>更新后的内容</p>"
        page.seo_title = "新标题 - SEO"
        db_session.commit()
        db_session.refresh(page)

        # 验证更新成功
        assert page.title == "新标题"
        assert page.content_markdown == "# 新内容\n\n更新后的内容"
        assert page.seo_title == "新标题 - SEO"


class TestSinglePageDelete:
    """测试单页删除功能"""

    def test_delete_page(self, db_session):
        """测试删除单页"""
        # 创建栏目和单页
        column = SiteColumn(
            name="待删除栏目",
            slug="to-delete",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
            show_in_nav=True,
            sort_order=0,
        )
        db_session.add(column)
        db_session.commit()

        page = SinglePage(
            column_id=column.id,
            title="待删除页面",
            slug="to-delete-page",
            content_markdown="待删除",
            content_html="<p>待删除</p>",
            status="draft",
        )
        db_session.add(page)
        db_session.commit()
        page_id = page.id

        # 删除单页
        db_session.delete(page)
        db_session.commit()

        # 验证删除成功
        deleted_page = db_session.query(SinglePage).filter_by(id=page_id).first()
        assert deleted_page is None
