"""
测试栏目 CRUD 功能

测试用例:
1. 创建基础栏目
2. 创建带父栏目的子栏目
3. Slug 自动生成
4. Slug 唯一性验证
5. 根据 ID 查询栏目
6. 根据 Slug 查询栏目
7. 查询所有栏目
8. 更新栏目基本信息
9. 更新栏目 Hero 配置
10. 切换栏目启用/禁用状态
11. 删除空栏目
12. 无法删除包含内容的栏目
"""

import pytest
from app.models.site import SiteColumn, ColumnType


class TestColumnCreate:
    """测试栏目创建功能"""

    def test_create_basic_column(self, db_session):
        """测试创建基础栏目"""
        # 创建栏目
        column = SiteColumn(
            name="关于我们",
            slug="about",
            column_type=ColumnType.SINGLE_PAGE,
            description="了解我们的团队和历史",
            is_enabled=True,
            show_in_nav=True,
            sort_order=0,
        )
        db_session.add(column)
        db_session.commit()
        db_session.refresh(column)

        # 验证创建成功
        assert column.id is not None
        assert column.name == "关于我们"
        assert column.slug == "about"
        assert column.column_type == ColumnType.SINGLE_PAGE
        assert column.description == "了解我们的团队和历史"
        assert column.is_enabled is True
        assert column.show_in_nav is True
        assert column.parent_id is None
        assert column.created_at is not None

    def test_create_column_with_parent(self, db_session):
        """测试创建带父栏目的子栏目"""
        # 创建父栏目
        parent = SiteColumn(
            name="关于我们",
            slug="about",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
        )
        db_session.add(parent)
        db_session.commit()
        db_session.refresh(parent)

        # 创建子栏目
        child = SiteColumn(
            name="团队介绍",
            slug="team",
            column_type=ColumnType.SINGLE_PAGE,
            parent_id=parent.id,
            is_enabled=True,
        )
        db_session.add(child)
        db_session.commit()
        db_session.refresh(child)

        # 验证父子关系
        assert child.id is not None
        assert child.parent_id == parent.id
        assert child.parent.id == parent.id
        assert child.parent.name == "关于我们"
        assert len(parent.children) == 1
        assert parent.children[0].id == child.id

    def test_slug_auto_generation(self, db_session):
        """测试 Slug 自动生成功能"""
        from app.services.column_service import generate_slug

        # 测试中文转 slug
        slug1 = generate_slug("关于我们", db_session)
        assert slug1 == "guan-yu-wo-men"

        # 测试英文转 slug
        slug2 = generate_slug("About Us", db_session)
        assert slug2 == "about-us"

        # 测试特殊字符处理
        slug3 = generate_slug("测试@#栏目!", db_session)
        assert "#" not in slug3
        assert "@" not in slug3
        assert "!" not in slug3

    def test_slug_uniqueness(self, db_session):
        """测试 Slug 唯一性保证"""
        from app.services.column_service import generate_slug

        # 创建第一个栏目
        column1 = SiteColumn(
            name="关于我们",
            slug="about",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
        )
        db_session.add(column1)
        db_session.commit()

        # 生成第二个栏目的 slug（同名）
        slug2 = generate_slug("关于我们", db_session)
        # 应该生成带数字后缀的唯一 slug
        assert slug2 != "about"
        assert slug2.startswith("about-") or slug2.startswith("guan-yu-wo-men")

        # 创建第二个栏目
        column2 = SiteColumn(
            name="关于我们",
            slug=slug2,
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
        )
        db_session.add(column2)
        db_session.commit()

        # 验证两个栏目的 slug 不同
        assert column1.slug != column2.slug


class TestColumnRead:
    """测试栏目查询功能"""

    def test_get_column_by_id(self, db_session):
        """测试根据 ID 查询栏目"""
        # 创建栏目
        column = SiteColumn(
            name="新闻动态", slug="news", column_type=ColumnType.POST, is_enabled=True
        )
        db_session.add(column)
        db_session.commit()

        # 查询栏目
        found = db_session.query(SiteColumn).filter_by(id=column.id).first()

        # 验证查询结果
        assert found is not None
        assert found.id == column.id
        assert found.name == "新闻动态"
        assert found.slug == "news"

    def test_get_column_by_slug(self, db_session):
        """测试根据 Slug 查询栏目"""
        # 创建栏目
        column = SiteColumn(
            name="产品中心",
            slug="products",
            column_type=ColumnType.PRODUCT,
            is_enabled=True,
        )
        db_session.add(column)
        db_session.commit()

        # 查询栏目
        found = db_session.query(SiteColumn).filter_by(slug="products").first()

        # 验证查询结果
        assert found is not None
        assert found.slug == "products"
        assert found.name == "产品中心"
        assert found.column_type == ColumnType.PRODUCT

    def test_get_all_columns(self, db_session):
        """测试查询所有栏目"""
        # 创建多个栏目
        columns_data = [
            {
                "name": "首页",
                "slug": "home",
                "type": ColumnType.SINGLE_PAGE,
                "order": 0,
            },
            {
                "name": "关于",
                "slug": "about",
                "type": ColumnType.SINGLE_PAGE,
                "order": 1,
            },
            {"name": "新闻", "slug": "news", "type": ColumnType.POST, "order": 2},
        ]

        for data in columns_data:
            column = SiteColumn(
                name=data["name"],
                slug=data["slug"],
                column_type=data["type"],
                sort_order=data["order"],
                is_enabled=True,
            )
            db_session.add(column)
        db_session.commit()

        # 查询所有栏目
        all_columns = db_session.query(SiteColumn).order_by(SiteColumn.sort_order).all()

        # 验证查询结果
        assert len(all_columns) == 3
        assert all_columns[0].name == "首页"
        assert all_columns[1].name == "关于"
        assert all_columns[2].name == "新闻"


class TestColumnUpdate:
    """测试栏目更新功能"""

    def test_update_basic_info(self, db_session):
        """测试更新栏目基本信息"""
        # 创建栏目
        column = SiteColumn(
            name="旧名称",
            slug="old-name",
            column_type=ColumnType.SINGLE_PAGE,
            description="旧描述",
            is_enabled=True,
        )
        db_session.add(column)
        db_session.commit()

        # 更新栏目
        column.name = "新名称"
        column.description = "新描述"
        db_session.commit()
        db_session.refresh(column)

        # 验证更新成功
        assert column.name == "新名称"
        assert column.description == "新描述"
        assert column.slug == "old-name"  # slug 不应自动改变
        assert column.updated_at is not None

    def test_update_hero_config(self, db_session):
        """测试更新栏目 Hero 配置"""
        # 创建栏目
        column = SiteColumn(
            name="首页",
            slug="home",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
        )
        db_session.add(column)
        db_session.commit()

        # 更新 Hero 配置
        column.hero_title = "欢迎来到我们的网站"
        column.hero_title_en = "Welcome to Our Website"
        column.hero_tagline = "专业、创新、卓越"
        column.hero_cta_text = "了解更多"
        column.hero_cta_url = "/about"
        db_session.commit()
        db_session.refresh(column)

        # 验证 Hero 配置
        assert column.hero_title == "欢迎来到我们的网站"
        assert column.hero_title_en == "Welcome to Our Website"
        assert column.hero_tagline == "专业、创新、卓越"
        assert column.hero_cta_text == "了解更多"
        assert column.hero_cta_url == "/about"

    def test_toggle_active_status(self, db_session):
        """测试切换栏目启用/禁用状态"""
        # 创建启用的栏目
        column = SiteColumn(
            name="测试栏目",
            slug="test",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
            show_in_nav=True,
        )
        db_session.add(column)
        db_session.commit()

        # 禁用栏目
        column.is_enabled = False
        db_session.commit()
        db_session.refresh(column)
        assert column.is_enabled is False

        # 重新启用栏目
        column.is_enabled = True
        db_session.commit()
        db_session.refresh(column)
        assert column.is_enabled is True


class TestColumnDelete:
    """测试栏目删除功能"""

    def test_delete_empty_column(self, db_session):
        """测试删除空栏目（无关联内容）"""
        # 创建栏目
        column = SiteColumn(
            name="待删除栏目",
            slug="to-delete",
            column_type=ColumnType.SINGLE_PAGE,
            is_enabled=True,
        )
        db_session.add(column)
        db_session.commit()
        column_id = column.id

        # 删除栏目
        db_session.delete(column)
        db_session.commit()

        # 验证删除成功
        deleted = db_session.query(SiteColumn).filter_by(id=column_id).first()
        assert deleted is None

    def test_cannot_delete_column_with_content(self, db_session):
        """测试无法删除包含内容的栏目"""
        from app.services.column_service import can_delete_column
        from app.models.post import Post

        # 创建栏目
        column = SiteColumn(
            name="新闻栏目", slug="news", column_type=ColumnType.POST, is_enabled=True
        )
        db_session.add(column)
        db_session.commit()

        # 创建文章关联到栏目
        post = Post(
            title="测试文章",
            slug="test-post",
            content_html="<p>测试内容</p>",
            column_id=column.id,
            status="published",
        )
        db_session.add(post)
        db_session.commit()

        # 检查是否可以删除
        can_delete = can_delete_column(db_session, column.id)

        # 验证无法删除
        assert can_delete is False
