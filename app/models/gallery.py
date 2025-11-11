"""相册模块模型"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Gallery(BaseModel):
    """
    相册模型

    管理相册集合，每个相册包含多张图片
    """

    __tablename__ = "gallery"

    title = Column(String(200), nullable=False, comment="相册标题")
    slug = Column(String(200), nullable=False, unique=True, comment="URL Slug")
    description = Column(Text, nullable=True, comment="相册描述")
    category = Column(String(100), nullable=True, comment="分类")
    tags = Column(String(255), nullable=True, comment="标签（逗号分隔）")
    cover_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="封面图ID"
    )
    display_mode = Column(
        String(50), default="grid", nullable=True, comment="展示模式: grid, masonry, carousel"
    )
    is_featured = Column(Boolean, default=False, nullable=False, comment="是否推荐")
    is_public = Column(Boolean, default=True, nullable=False, comment="是否公开")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    allow_download = Column(Boolean, default=False, nullable=False, comment="允许下载")
    watermark_enabled = Column(Boolean, default=False, nullable=False, comment="启用水印")
    seo_title = Column(String(200), nullable=True, comment="SEO标题")
    seo_description = Column(Text, nullable=True, comment="SEO描述")
    view_count = Column(Integer, default=0, nullable=False, comment="浏览次数")
    image_count = Column(Integer, default=0, nullable=False, comment="图片数量")
    notes = Column(Text, nullable=True, comment="内部备注")

    # 关系
    cover_media = relationship("MediaFile", foreign_keys=[cover_media_id])
    images = relationship(
        "GalleryImage",
        back_populates="gallery",
        order_by="GalleryImage.sort_order",
        cascade="all, delete-orphan"
    )


class GalleryImage(BaseModel):
    """
    相册图片模型

    相册中的单张图片
    """

    __tablename__ = "gallery_image"

    gallery_id = Column(
        Integer, ForeignKey("gallery.id"), nullable=False, comment="相册ID"
    )
    media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=False, comment="媒体文件ID"
    )
    title = Column(String(200), nullable=True, comment="图片标题")
    caption = Column(Text, nullable=True, comment="图片说明")
    alt_text = Column(String(255), nullable=True, comment="替代文本")
    tags = Column(String(255), nullable=True, comment="标签（逗号分隔）")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_visible = Column(Boolean, default=True, nullable=False, comment="是否可见")
    is_featured = Column(Boolean, default=False, nullable=False, comment="是否推荐")
    link_url = Column(String(500), nullable=True, comment="链接地址")
    link_target = Column(
        String(20), default="_self", nullable=True, comment="链接打开方式"
    )
    view_count = Column(Integer, default=0, nullable=False, comment="浏览次数")
    download_count = Column(Integer, default=0, nullable=False, comment="下载次数")
    notes = Column(Text, nullable=True, comment="内部备注")

    # 关系
    gallery = relationship("Gallery", back_populates="images")
    media = relationship("MediaFile", foreign_keys=[media_id])
