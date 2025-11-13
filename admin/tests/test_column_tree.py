"""
测试栏目树形结构功能

测试用例:
1. 构建栏目树形结构
2. 获取导航显示的栏目
3. 获取底部显示的栏目
"""

import pytest
from app.models.site import SiteColumn, ColumnType


class TestColumnTree:
    """测试栏目树形结构功能"""

    def test_build_tree_structure(self, db_session):
        """测试构建栏目树形结构"""
        from app.services.column_service import build_tree

        # 创建树形栏目结构
        # 关于我们 (1)
        #   ├── 团队介绍 (2)
        #   └── 联系方式 (3)
        # 新闻动态 (4)
        #   └── 公司新闻 (5)
        # 产品中心 (6)

        # 创建顶级栏目
        about = SiteColumn(
            name="关于我们",
            slug="about",
            column_type=ColumnType.SINGLE_PAGE,
            sort_order=1,
            is_enabled=True,
        )
        news = SiteColumn(
            name="新闻动态",
            slug="news",
            column_type=ColumnType.POST,
            sort_order=2,
            is_enabled=True,
        )
        products = SiteColumn(
            name="产品中心",
            slug="products",
            column_type=ColumnType.PRODUCT,
            sort_order=3,
            is_enabled=True,
        )
        db_session.add_all([about, news, products])
        db_session.commit()

        # 创建子栏目
        team = SiteColumn(
            name="团队介绍",
            slug="team",
            column_type=ColumnType.SINGLE_PAGE,
            parent_id=about.id,
            sort_order=1,
            is_enabled=True,
        )
        contact = SiteColumn(
            name="联系方式",
            slug="contact",
            column_type=ColumnType.SINGLE_PAGE,
            parent_id=about.id,
            sort_order=2,
            is_enabled=True,
        )
        company_news = SiteColumn(
            name="公司新闻",
            slug="company-news",
            column_type=ColumnType.POST,
            parent_id=news.id,
            sort_order=1,
            is_enabled=True,
        )
        db_session.add_all([team, contact, company_news])
        db_session.commit()

        # 构建树形结构
        tree = build_tree(db_session)

        # 验证树形结构
        assert len(tree) == 3  # 3个顶级栏目

        # 验证第一个顶级栏目（关于我们）
        assert tree[0]["name"] == "关于我们"
        assert tree[0]["slug"] == "about"
        assert len(tree[0]["children"]) == 2
        assert tree[0]["children"][0]["name"] == "团队介绍"
        assert tree[0]["children"][1]["name"] == "联系方式"

        # 验证第二个顶级栏目（新闻动态）
        assert tree[1]["name"] == "新闻动态"
        assert tree[1]["slug"] == "news"
        assert len(tree[1]["children"]) == 1
        assert tree[1]["children"][0]["name"] == "公司新闻"

        # 验证第三个顶级栏目（产品中心）
        assert tree[2]["name"] == "产品中心"
        assert tree[2]["slug"] == "products"
        assert len(tree[2]["children"]) == 0

    def test_get_nav_columns(self, db_session):
        """测试获取导航显示的栏目"""
        from app.services.column_service import get_nav_columns

        # 创建栏目
        # 显示在导航的栏目
        nav1 = SiteColumn(
            name="首页",
            slug="home",
            column_type=ColumnType.SINGLE_PAGE,
            show_in_nav=True,
            is_enabled=True,
            sort_order=1,
        )
        nav2 = SiteColumn(
            name="关于",
            slug="about",
            column_type=ColumnType.SINGLE_PAGE,
            show_in_nav=True,
            is_enabled=True,
            sort_order=2,
        )

        # 不显示在导航的栏目
        no_nav = SiteColumn(
            name="隐藏页面",
            slug="hidden",
            column_type=ColumnType.SINGLE_PAGE,
            show_in_nav=False,
            is_enabled=True,
            sort_order=3,
        )

        # 已禁用的栏目
        disabled = SiteColumn(
            name="已禁用",
            slug="disabled",
            column_type=ColumnType.SINGLE_PAGE,
            show_in_nav=True,
            is_enabled=False,
            sort_order=4,
        )

        db_session.add_all([nav1, nav2, no_nav, disabled])
        db_session.commit()

        # 获取导航栏目
        nav_columns = get_nav_columns(db_session)

        # 验证结果
        assert len(nav_columns) == 2
        assert nav_columns[0].name == "首页"
        assert nav_columns[1].name == "关于"

        # 验证排序
        assert nav_columns[0].sort_order < nav_columns[1].sort_order

    def test_get_footer_columns(self, db_session):
        """测试获取底部显示的栏目"""
        from app.services.column_service import get_footer_columns

        # 创建栏目
        # 使用 menu_location 字段
        footer1 = SiteColumn(
            name="关于我们",
            slug="about",
            column_type=ColumnType.SINGLE_PAGE,
            menu_location="footer",
            is_enabled=True,
            sort_order=1,
        )
        footer2 = SiteColumn(
            name="联系我们",
            slug="contact",
            column_type=ColumnType.SINGLE_PAGE,
            menu_location="footer",
            is_enabled=True,
            sort_order=2,
        )
        both = SiteColumn(
            name="新闻",
            slug="news",
            column_type=ColumnType.POST,
            menu_location="both",
            is_enabled=True,
            sort_order=3,
        )

        # 只在 header 显示
        header_only = SiteColumn(
            name="产品",
            slug="products",
            column_type=ColumnType.PRODUCT,
            menu_location="header",
            is_enabled=True,
            sort_order=4,
        )

        # 不显示在任何位置
        none = SiteColumn(
            name="隐藏",
            slug="hidden",
            column_type=ColumnType.SINGLE_PAGE,
            menu_location="none",
            is_enabled=True,
            sort_order=5,
        )

        db_session.add_all([footer1, footer2, both, header_only, none])
        db_session.commit()

        # 获取底部栏目
        footer_columns = get_footer_columns(db_session)

        # 验证结果（应该包含 menu_location 为 "footer" 和 "both" 的栏目）
        assert len(footer_columns) == 3
        names = [col.name for col in footer_columns]
        assert "关于我们" in names
        assert "联系我们" in names
        assert "新闻" in names
        assert "产品" not in names
        assert "隐藏" not in names

        # 验证排序
        assert footer_columns[0].sort_order == 1
        assert footer_columns[1].sort_order == 2
        assert footer_columns[2].sort_order == 3
