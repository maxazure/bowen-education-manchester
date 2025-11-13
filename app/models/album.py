"""
相册管理模型

包含三个模型：
1. AlbumCategory - 相册分类
2. Album - 相册
3. AlbumPhoto - 相册照片关联
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class AlbumCategory(BaseModel):
    """相册分类模型"""

    __tablename__ = "album_category"

    name = Column(String(100), nullable=False, comment="分类名称")
    slug = Column(String(100), unique=True, comment="URL Slug")
    description = Column(Text, comment="分类描述")
    sort_order = Column(Integer, default=0, comment="排序")
    is_enabled = Column(Boolean, default=True, comment="是否启用")

    # 关系
    albums = relationship(
        "Album",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<AlbumCategory {self.name}>"


class Album(BaseModel):
    """相册模型"""

    __tablename__ = "album"

    # 基本信息
    title = Column(String(200), nullable=False, comment="相册标题")
    slug = Column(String(200), unique=True, comment="URL Slug")
    description = Column(Text, comment="相册描述")
    cover_media_id = Column(
        Integer, ForeignKey("media_file.id", ondelete="SET NULL"), comment="封面图ID"
    )

    # 分类和标签
    category_id = Column(
        Integer, ForeignKey("album_category.id", ondelete="SET NULL"), comment="分类ID"
    )
    tags = Column(String(500), comment="标签（JSON 数组）")

    # 统计信息
    photo_count = Column(Integer, default=0, comment="照片数量")
    view_count = Column(Integer, default=0, comment="浏览次数")

    # 排序和状态
    sort_order = Column(Integer, default=0, comment="排序")
    status = Column(String(20), default="draft", comment="状态: draft/published")

    # SEO 信息
    seo_title = Column(String(200), comment="SEO 标题")
    seo_description = Column(Text, comment="SEO 描述")
    seo_keywords = Column(String(500), comment="SEO 关键词")

    # 时间戳
    published_at = Column(DateTime, comment="发布时间")

    # 关系
    category = relationship("AlbumCategory", back_populates="albums")
    cover_media = relationship("MediaFile", foreign_keys=[cover_media_id])
    photos = relationship(
        "AlbumPhoto",
        back_populates="album",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="AlbumPhoto.sort_order",
    )

    @property
    def is_published(self) -> bool:
        """是否已发布"""
        return self.status == "published"

    @property
    def category_name(self) -> Optional[str]:
        """分类名称"""
        return self.category.name if self.category else None

    @property
    def tags_list(self) -> list:
        """标签列表"""
        if not self.tags:
            return []
        import json

        try:
            return json.loads(self.tags)
        except:
            return []

    def publish(self):
        """发布相册"""
        self.status = "published"
        if not self.published_at:
            self.published_at = datetime.now()

    def unpublish(self):
        """取消发布"""
        self.status = "draft"

    def __repr__(self):
        return f"<Album {self.title}>"


class AlbumPhoto(BaseModel):
    """相册照片关联模型"""

    __tablename__ = "album_photo"

    album_id = Column(
        Integer, ForeignKey("album.id", ondelete="CASCADE"), nullable=False, comment="相册ID"
    )
    media_id = Column(
        Integer,
        ForeignKey("media_file.id", ondelete="CASCADE"),
        nullable=False,
        comment="媒体文件ID",
    )
    caption = Column(Text, comment="照片说明")
    sort_order = Column(Integer, default=0, comment="排序")

    # 关系
    album = relationship("Album", back_populates="photos")
    media = relationship("MediaFile")

    @property
    def media_url(self) -> Optional[str]:
        """媒体文件 URL"""
        return self.media.path_original if self.media else None

    @property
    def thumbnail_url(self) -> Optional[str]:
        """缩略图 URL"""
        return self.media.path_thumb if self.media else None

    def __repr__(self):
        return f"<AlbumPhoto album_id={self.album_id} media_id={self.media_id}>"
