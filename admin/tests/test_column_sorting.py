"""
测试栏目排序功能

测试用例:
1. 默认排序顺序
2. 手动设置排序顺序
3. 批量更新排序顺序
"""

import pytest
from app.models.site import SiteColumn, ColumnType


class TestColumnSorting:
    """测试栏目排序功能"""

    def test_default_sort_order(self, db_session):
        """测试默认排序顺序"""
        # 创建多个栏目（不指定 sort_order）
        columns = [
            SiteColumn(
                name="首页",
                slug="home",
                column_type=ColumnType.SINGLE_PAGE,
                is_enabled=True,
            ),
            SiteColumn(
                name="关于",
                slug="about",
                column_type=ColumnType.SINGLE_PAGE,
                is_enabled=True,
            ),
            SiteColumn(
                name="新闻", slug="news", column_type=ColumnType.POST, is_enabled=True
            ),
        ]

        for column in columns:
            db_session.add(column)
        db_session.commit()

        # 查询栏目（按 sort_order 排序）
        sorted_columns = (
            db_session.query(SiteColumn)
            .order_by(SiteColumn.sort_order, SiteColumn.id)
            .all()
        )

        # 验证默认排序值为 0
        for column in sorted_columns:
            assert column.sort_order == 0

        # 验证结果数量
        assert len(sorted_columns) == 3

    def test_manual_sort_order(self, db_session):
        """测试手动设置排序顺序"""
        # 创建多个栏目并设置不同的 sort_order
        columns_data = [
            {"name": "首页", "slug": "home", "order": 1},
            {"name": "关于", "slug": "about", "order": 2},
            {"name": "新闻", "slug": "news", "order": 3},
            {"name": "联系", "slug": "contact", "order": 4},
        ]

        for data in columns_data:
            column = SiteColumn(
                name=data["name"],
                slug=data["slug"],
                column_type=ColumnType.SINGLE_PAGE,
                sort_order=data["order"],
                is_enabled=True,
            )
            db_session.add(column)
        db_session.commit()

        # 查询栏目（按 sort_order 排序）
        sorted_columns = (
            db_session.query(SiteColumn).order_by(SiteColumn.sort_order).all()
        )

        # 验证排序顺序
        assert len(sorted_columns) == 4
        assert sorted_columns[0].name == "首页"
        assert sorted_columns[0].sort_order == 1
        assert sorted_columns[1].name == "关于"
        assert sorted_columns[1].sort_order == 2
        assert sorted_columns[2].name == "新闻"
        assert sorted_columns[2].sort_order == 3
        assert sorted_columns[3].name == "联系"
        assert sorted_columns[3].sort_order == 4

    def test_batch_update_sort_order(self, db_session):
        """测试批量更新排序顺序"""
        # 创建多个栏目
        columns = []
        for i, name in enumerate(["A", "B", "C", "D"], start=1):
            column = SiteColumn(
                name=name,
                slug=name.lower(),
                column_type=ColumnType.SINGLE_PAGE,
                sort_order=i,
                is_enabled=True,
            )
            db_session.add(column)
            columns.append(column)
        db_session.commit()

        # 批量更新排序（反转顺序）
        # A(1) -> A(4), B(2) -> B(3), C(3) -> C(2), D(4) -> D(1)
        new_order = [
            {"id": columns[0].id, "sort_order": 4},
            {"id": columns[1].id, "sort_order": 3},
            {"id": columns[2].id, "sort_order": 2},
            {"id": columns[3].id, "sort_order": 1},
        ]

        for item in new_order:
            column = db_session.query(SiteColumn).filter_by(id=item["id"]).first()
            if column:
                column.sort_order = item["sort_order"]
        db_session.commit()

        # 查询验证新排序
        sorted_columns = (
            db_session.query(SiteColumn).order_by(SiteColumn.sort_order).all()
        )

        # 验证新排序顺序
        assert len(sorted_columns) == 4
        assert sorted_columns[0].name == "D"
        assert sorted_columns[0].sort_order == 1
        assert sorted_columns[1].name == "C"
        assert sorted_columns[1].sort_order == 2
        assert sorted_columns[2].name == "B"
        assert sorted_columns[2].sort_order == 3
        assert sorted_columns[3].name == "A"
        assert sorted_columns[3].sort_order == 4
