"""文章/博客相关模型"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import BaseModel


class PostCategory(BaseModel):
    """
    文章分类模型

    支持多级分类，按栏目隔离
    """

    __tablename__ = "post_category"

    column_id = Column(
        Integer, ForeignKey("site_column.id"), nullable=False, comment="关联栏目ID"
    )
    parent_id = Column(
        Integer, ForeignKey("post_category.id"), nullable=True, comment="父分类ID"
    )
    name = Column(String(100), nullable=False, comment="分类名称")
    slug = Column(String(100), nullable=False, comment="分类Slug")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_visible = Column(Boolean, default=True, nullable=False, comment="是否可见")

    # 关系
    column = relationship("SiteColumn", backref="post_categories")
    parent = relationship(
        "PostCategory", remote_side="PostCategory.id", backref="children"
    )


class Post(BaseModel):
    """
    文章模型

    用于资讯、博客、新闻等内容
    """

    __tablename__ = "post"

    column_id = Column(
        Integer, ForeignKey("site_column.id"), nullable=False, comment="关联栏目ID"
    )
    title = Column(String(200), nullable=False, comment="文章标题")
    slug = Column(String(200), nullable=False, comment="文章Slug")
    summary = Column(Text, nullable=True, comment="文章摘要")
    cover_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="封面图ID"
    )
    content_html = Column(Text, nullable=False, comment="文章内容HTML")
    is_recommended = Column(Boolean, default=False, nullable=False, comment="是否推荐")
    status = Column(
        Enum("draft", "published", "offline", name="post_status"),
        default="draft",
        nullable=False,
        comment="状态",
    )
    seo_title = Column(String(200), nullable=True, comment="SEO标题")
    seo_description = Column(Text, nullable=True, comment="SEO描述")
    published_at = Column(DateTime, nullable=True, comment="发布时间")
    is_approved = Column(Integer, default=0, nullable=False, comment="是否已审核通过(0=待审核,1=已通过)")
    admin_reply = Column(Text, nullable=True, comment="管理员回复内容")

    # 关系
    column = relationship("SiteColumn", backref="posts")
    cover_media = relationship("MediaFile", foreign_keys=[cover_media_id])
    categories = relationship(
        "PostCategory", secondary="post_category_link", backref="posts"
    )

    @property
    def featured_image(self):
        """Get the featured image URL for this article"""
        if self.cover_media:
            return self.cover_media.file_url
        # Fallback to static image based on slug
        return f"/static/images/article-{self.slug}-featured.jpg"


class PostCategoryLink(Base):
    """
    文章与分类的多对多关联表
    """

    __tablename__ = "post_category_link"

    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True, comment="文章ID")
    category_id = Column(
        Integer, ForeignKey("post_category.id"), primary_key=True, comment="分类ID"
    )
