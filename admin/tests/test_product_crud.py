"""
测试产品 CRUD 功能
"""


from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.site import ColumnType, SiteColumn


def test_create_product(db_session: Session):
    """测试创建产品"""
    # 创建测试数据
    column = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建产品
    product = Product(
        column_id=column.id,
        name="测试产品",
        slug="test-product",
        summary="这是一个测试产品",
        description_html="<h1>产品详情</h1><p>这是详细描述</p>",
        price_text="¥999",
        availability_status="in_stock",
        status="draft",
    )
    db_session.add(product)
    db_session.commit()

    # 验证
    assert product.id is not None
    assert product.name == "测试产品"
    assert product.slug == "test-product"
    assert product.summary == "这是一个测试产品"
    assert product.price_text == "¥999"
    assert product.availability_status == "in_stock"
    assert product.status == "draft"
    assert product.is_recommended is False


def test_set_price(db_session: Session):
    """测试设置价格（原价、现价）"""
    # 创建栏目
    column = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建产品并设置价格
    product = Product(
        column_id=column.id,
        name="价格测试产品",
        slug="price-test-product",
        description_html="<p>内容</p>",
        price_text="¥1999 (原价 ¥2999)",
    )
    db_session.add(product)
    db_session.commit()

    # 验证价格设置
    assert product.price_text == "¥1999 (原价 ¥2999)"

    # 修改价格
    product.price_text = "¥1599"
    db_session.commit()

    db_session.refresh(product)
    assert product.price_text == "¥1599"


def test_set_attributes(db_session: Session):
    """测试设置产品属性（库存、单位、规格等）"""
    # 创建栏目
    column = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    # 创建产品并设置属性
    product = Product(
        column_id=column.id,
        name="属性测试产品",
        slug="attributes-test-product",
        description_html="<p>内容</p>",
        price_text="¥899",
        availability_status="in_stock",
    )
    db_session.add(product)
    db_session.commit()

    # 验证属性
    assert product.availability_status == "in_stock"

    # 修改为缺货
    product.availability_status = "out_of_stock"
    db_session.commit()

    db_session.refresh(product)
    assert product.availability_status == "out_of_stock"

    # 修改为询价
    product.availability_status = "inquiry"
    db_session.commit()

    db_session.refresh(product)
    assert product.availability_status == "inquiry"


def test_update_product(db_session: Session):
    """测试更新产品"""
    # 创建栏目和产品
    column = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    product = Product(
        column_id=column.id,
        name="原产品名",
        slug="original-product",
        summary="原摘要",
        description_html="<h1>原内容</h1>",
        price_text="¥999",
        status="draft",
    )
    db_session.add(product)
    db_session.commit()

    # 更新产品
    product.name = "新产品名"
    product.slug = "new-product"
    product.summary = "新摘要"
    product.description_html = "<h1>新内容</h1>"
    product.price_text = "¥1999"
    product.is_recommended = True
    db_session.commit()

    # 验证
    db_session.refresh(product)
    assert product.name == "新产品名"
    assert product.slug == "new-product"
    assert product.summary == "新摘要"
    assert product.description_html == "<h1>新内容</h1>"
    assert product.price_text == "¥1999"
    assert product.is_recommended is True


def test_delete_product(db_session: Session):
    """测试删除产品"""
    # 创建栏目和产品
    column = SiteColumn(
        name="产品中心",
        slug="products",
        column_type=ColumnType.PRODUCT,
        sort_order=1,
    )
    db_session.add(column)
    db_session.commit()

    product = Product(
        column_id=column.id,
        name="待删除产品",
        slug="to-delete",
        description_html="<p>内容</p>",
    )
    db_session.add(product)
    db_session.commit()

    product_id = product.id

    # 删除产品
    db_session.delete(product)
    db_session.commit()

    # 验证
    deleted_product = db_session.query(Product).filter(Product.id == product_id).first()
    assert deleted_product is None
