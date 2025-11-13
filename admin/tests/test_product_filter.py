"""
测试产品筛选功能
"""

from sqlalchemy.orm import Session

from app.models.product import Product, ProductCategory
from app.models.site import ColumnType, SiteColumn


def test_filter_by_column(db_session: Session):
    """测试按栏目筛选"""
    # 创建两个栏目
    column1 = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    column2 = SiteColumn(
        name="解决方案",
        slug="solutions",
        column_type=ColumnType.PRODUCT,
        sort_order=2,
    )
    db_session.add_all([column1, column2])
    db_session.commit()

    # 创建产品
    product1 = Product(
        column_id=column1.id,
        name="产品1",
        slug="product-1",
        description_html="<p>内容</p>",
    )
    product2 = Product(
        column_id=column1.id,
        name="产品2",
        slug="product-2",
        description_html="<p>内容</p>",
    )
    product3 = Product(
        column_id=column2.id,
        name="解决方案1",
        slug="solution-1",
        description_html="<p>内容</p>",
    )
    db_session.add_all([product1, product2, product3])
    db_session.commit()

    # 筛选 column1 的产品
    products_col1 = (
        db_session.query(Product).filter(Product.column_id == column1.id).all()
    )
    assert len(products_col1) == 2

    # 筛选 column2 的产品
    products_col2 = (
        db_session.query(Product).filter(Product.column_id == column2.id).all()
    )
    assert len(products_col2) == 1


def test_filter_by_category(db_session: Session):
    """测试按分类筛选"""
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
    db_session.add_all([cat1, cat2])
    db_session.commit()

    # 创建产品
    product1 = Product(
        column_id=column.id,
        name="产品1",
        slug="product-1",
        description_html="<p>内容</p>",
    )
    product2 = Product(
        column_id=column.id,
        name="产品2",
        slug="product-2",
        description_html="<p>内容</p>",
    )
    product3 = Product(
        column_id=column.id,
        name="产品3",
        slug="product-3",
        description_html="<p>内容</p>",
    )

    # 设置分类
    product1.categories.append(cat1)
    product2.categories.append(cat1)
    product2.categories.append(cat2)
    product3.categories.append(cat2)

    db_session.add_all([product1, product2, product3])
    db_session.commit()

    # 筛选智能设备分类
    products_cat1 = (
        db_session.query(Product)
        .join(Product.categories)
        .filter(ProductCategory.id == cat1.id)
        .all()
    )
    assert len(products_cat1) == 2

    # 筛选环保产品分类
    products_cat2 = (
        db_session.query(Product)
        .join(Product.categories)
        .filter(ProductCategory.id == cat2.id)
        .all()
    )
    assert len(products_cat2) == 2


def test_search(db_session: Session):
    """测试搜索产品"""
    # 创建栏目
    column = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建产品
    product1 = Product(
        column_id=column.id,
        name="智能温控器",
        slug="smart-thermostat",
        summary="智能家居温控设备",
        description_html="<p>内容</p>",
    )
    product2 = Product(
        column_id=column.id,
        name="节能LED灯",
        slug="led-light",
        summary="节能环保照明",
        description_html="<p>内容</p>",
    )
    product3 = Product(
        column_id=column.id,
        name="空气净化器",
        slug="air-purifier",
        summary="智能空气净化",
        description_html="<p>内容</p>",
    )
    db_session.add_all([product1, product2, product3])
    db_session.commit()

    # 搜索"智能"
    keyword = "智能"
    results = (
        db_session.query(Product)
        .filter((Product.name.contains(keyword)) | (Product.summary.contains(keyword)))
        .all()
    )
    assert len(results) == 2

    # 搜索"节能"
    keyword = "节能"
    results = (
        db_session.query(Product)
        .filter((Product.name.contains(keyword)) | (Product.summary.contains(keyword)))
        .all()
    )
    assert len(results) == 1
