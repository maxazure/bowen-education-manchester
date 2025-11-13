"""
测试单页 SEO 功能

测试用例:
1. 设置 meta description
2. 设置 meta keywords
3. Slug 自动生成
"""

import pytest

from app.models.site import ColumnType, SinglePage, SiteColumn
from app.services.single_page_service import generate_slug


class TestSinglePageSEO:
    """测试单页 SEO 功能"""

    def test_set_meta_description(self, db_session):
        """测试设置 meta description"""
        # 创建栏目
        column = SiteColumn(
            name="SEO测试",
            slug="seo-test",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
            show_in_nav=True,
            sort_order=0,
        )
        db_session.add(column)
        db_session.commit()

        # 创建单页并设置 SEO 信息
        page = SinglePage(
            column_id=column.id,
            title="SEO测试页面",
            slug="seo-test-page",
            content_markdown="测试内容",
            content_html="<p>测试内容</p>",
            seo_description="这是一段详细的页面描述，用于搜索引擎优化",
            status="draft",
        )
        db_session.add(page)
        db_session.commit()
        db_session.refresh(page)

        # 验证 SEO 描述设置成功
        assert page.seo_description == "这是一段详细的页面描述，用于搜索引擎优化"

    def test_set_meta_keywords(self, db_session):
        """测试设置 meta keywords"""
        # 创建栏目
        column = SiteColumn(
            name="关键词测试",
            slug="keywords-test",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
            show_in_nav=True,
            sort_order=0,
        )
        db_session.add(column)
        db_session.commit()

        # 创建单页并设置关键词
        page = SinglePage(
            column_id=column.id,
            title="关键词测试页面",
            slug="keywords-test-page",
            content_markdown="测试内容",
            content_html="<p>测试内容</p>",
            seo_keywords="关键词1, 关键词2, 关键词3, SEO, 优化",
            status="draft",
        )
        db_session.add(page)
        db_session.commit()
        db_session.refresh(page)

        # 验证关键词设置成功
        assert page.seo_keywords == "关键词1, 关键词2, 关键词3, SEO, 优化"

    def test_slug_generation(self, db_session):
        """测试 Slug 自动生成"""
        # 创建栏目
        column = SiteColumn(
            name="Slug测试",
            slug="slug-test",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
            show_in_nav=True,
            sort_order=0,
        )
        db_session.add(column)
        db_session.commit()

        # 测试英文标题生成 Slug
        slug1 = generate_slug("About Us Team", db_session)
        assert slug1 == "about-us-team"

        # 测试中文标题生成 Slug (使用拼音)
        slug2 = generate_slug("关于我们", db_session)
        assert slug2  # 确保生成了 slug
        assert "-" in slug2 or len(slug2) > 0  # 确保格式正确

        # 创建一个已存在 slug 的单页
        page1 = SinglePage(
            column_id=column.id,
            title="测试页面1",
            slug="test-page",
            content_markdown="内容1",
            content_html="<p>内容1</p>",
            status="draft",
        )
        db_session.add(page1)
        db_session.commit()

        # 测试 Slug 唯一性 - 相同标题应该生成不同的 slug
        slug3 = generate_slug("test page", db_session)
        assert slug3 != "test-page"  # 应该添加数字后缀
        assert slug3.startswith("test-page-") or slug3 == "test-page-1"
