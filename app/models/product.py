"""产品相关模型"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import BaseModel


class ProductCategory(BaseModel):
    """
    产品分类模型

    支持多级分类，按栏目隔离
    """

    __tablename__ = "product_category"

    column_id = Column(
        Integer, ForeignKey("site_column.id"), nullable=False, comment="关联栏目ID"
    )
    parent_id = Column(
        Integer, ForeignKey("product_category.id"), nullable=True, comment="父分类ID"
    )
    name = Column(String(100), nullable=False, comment="分类名称")
    slug = Column(String(100), nullable=False, comment="分类Slug")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_visible = Column(Boolean, default=True, nullable=False, comment="是否可见")

    # 关系
    column = relationship("SiteColumn", backref="product_categories")
    parent = relationship(
        "ProductCategory", remote_side="ProductCategory.id", backref="children"
    )


class Product(BaseModel):
    """
    产品模型

    用于产品展示、解决方案等
    """

    __tablename__ = "product"

    column_id = Column(
        Integer, ForeignKey("site_column.id"), nullable=False, comment="关联栏目ID"
    )
    name = Column(String(200), nullable=False, comment="产品名称")
    slug = Column(String(200), nullable=False, comment="产品Slug")
    summary = Column(Text, nullable=True, comment="产品卖点/简述")
    description_html = Column(Text, nullable=False, comment="详细说明HTML")
    cover_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="封面图ID"
    )
    price_text = Column(String(100), nullable=True, comment="价格文本")
    availability_status = Column(
        Enum("in_stock", "out_of_stock", "inquiry", name="product_availability"),
        default="in_stock",
        nullable=False,
        comment="供货状态",
    )
    is_recommended = Column(Boolean, default=False, nullable=False, comment="是否推荐")
    status = Column(
        Enum("draft", "online", "offline", name="product_status"),
        default="draft",
        nullable=False,
        comment="状态",
    )
    seo_title = Column(String(200), nullable=True, comment="SEO标题")
    seo_description = Column(Text, nullable=True, comment="SEO描述")
    published_at = Column(DateTime, nullable=True, comment="上线时间")

    # 关系
    column = relationship("SiteColumn", backref="products")
    cover_media = relationship("MediaFile", foreign_keys=[cover_media_id])
    categories = relationship(
        "ProductCategory", secondary="product_category_link", backref="products"
    )

    @property
    def featured_image(self):
        """Get the featured image URL for this course"""
        if self.cover_media:
            return self.cover_media.file_url
        # Fallback to static image based on slug
        return f"/static/images/course-{self.slug}.jpg"


class ProductCategoryLink(Base):
    """
    产品与分类的多对多关联表
    """

    __tablename__ = "product_category_link"

    product_id = Column(
        Integer, ForeignKey("product.id"), primary_key=True, comment="产品ID"
    )
    category_id = Column(
        Integer, ForeignKey("product_category.id"), primary_key=True, comment="分类ID"
    )
