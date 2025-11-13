"""
测试产品分类功能
"""

from sqlalchemy.orm import Session

from app.models.product import Product, ProductCategory
from app.models.site import ColumnType, SiteColumn


def test_create_category(db_session: Session):
    """测试创建产品分类"""
    # 创建栏目
    column = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建分类
    category = ProductCategory(
        column_id=column.id,
        name="智能设备",
        slug="smart-devices",
        sort_order=1,
    )
    db_session.add(category)
    db_session.commit()

    # 验证
    assert category.id is not None
    assert category.name == "智能设备"
    assert category.slug == "smart-devices"
    assert category.column_id == column.id
    assert category.is_visible is True


def test_assign_categories(db_session: Session):
    """测试分配分类"""
    # 创建栏目
    column = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建分类
    category = ProductCategory(
        column_id=column.id,
        name="智能设备",
        slug="smart-devices",
    )
    db_session.add(category)
    db_session.commit()

    # 创建产品
    product = Product(
        column_id=column.id,
        name="测试产品",
        slug="test-product",
        description_html="<p>内容</p>",
    )
    db_session.add(product)
    db_session.commit()

    # 分配分类（多对多关系）
    product.categories.append(category)
    db_session.commit()

    # 验证
    db_session.refresh(product)
    assert len(product.categories) == 1
    assert product.categories[0].name == "智能设备"


def test_multi_select_categories(db_session: Session):
    """测试多选分类"""
    # 创建栏目和分类
    column = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    cat1 = ProductCategory(
        column_id=column.id,
        name="智能设备",
        slug="smart-devices",
    )
    cat2 = ProductCategory(
        column_id=column.id,
        name="环保产品",
        slug="eco-products",
    )
    cat3 = ProductCategory(
        column_id=column.id,
        name="节能产品",
        slug="energy-saving",
    )
    db_session.add_all([cat1, cat2, cat3])
    db_session.commit()

    # 创建产品
    product = Product(
        column_id=column.id,
        name="测试产品",
        slug="test-product",
        description_html="<p>内容</p>",
    )
    db_session.add(product)
    db_session.commit()

    # 设置多个分类（多对多关系）
    product.categories.append(cat1)
    product.categories.append(cat2)
    product.categories.append(cat3)
    db_session.commit()

    # 验证
    db_session.refresh(product)
    assert len(product.categories) == 3
    category_names = [c.name for c in product.categories]
    assert "智能设备" in category_names
    assert "环保产品" in category_names
    assert "节能产品" in category_names
