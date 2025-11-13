"""媒体文件模型"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class MediaFolder(BaseModel):
    """
    媒体文件夹模型

    用于组织和分类媒体文件
    """

    __tablename__ = "media_folder"

    name = Column(String(100), nullable=False, comment="文件夹名称")
    parent_id = Column(Integer, ForeignKey("media_folder.id", ondelete="CASCADE"), nullable=True, comment="父文件夹ID")
    path = Column(String(500), nullable=False, comment="文件夹路径")
    description = Column(Text, nullable=True, comment="描述")
    sort_order = Column(Integer, default=0, comment="排序")

    # 关系
    parent = relationship("MediaFolder", remote_side="MediaFolder.id", backref="children")
    files = relationship("MediaFile", back_populates="folder", cascade="all, delete-orphan")


class MediaFile(BaseModel):
    """
    媒体文件模型

    统一管理上传的图片、视频和文档
    """

    __tablename__ = "media_file"

    # 基本信息
    filename_original = Column(String(255), nullable=False, comment="原始文件名")
    mime_type = Column(String(100), nullable=False, comment="MIME类型")
    size_bytes = Column(Integer, nullable=False, comment="文件大小（字节）")

    # 文件路径
    path_original = Column(String(500), nullable=False, comment="原图路径")
    path_medium = Column(String(500), nullable=True, comment="中等尺寸图路径")
    path_thumb = Column(String(500), nullable=True, comment="缩略图路径")

    # 图片专用字段
    width = Column(Integer, nullable=True, comment="图片宽度")
    height = Column(Integer, nullable=True, comment="图片高度")

    # 视频专用字段
    duration = Column(Integer, nullable=True, comment="视频时长（秒）")
    video_thumbnail_path = Column(String(500), nullable=True, comment="视频缩略图路径")

    # 分类和组织
    file_type = Column(String(50), default="image", comment="文件类型（image/video/document/other）")
    folder_id = Column(Integer, ForeignKey("media_folder.id", ondelete="SET NULL"), nullable=True, comment="所属文件夹ID")
    tags = Column(String(500), nullable=True, comment="标签（JSON数组）")

    # 元数据和SEO
    title = Column(String(255), nullable=True, comment="媒体标题")
    alt_text = Column(String(255), nullable=True, comment="Alt 文本（SEO）")
    caption = Column(Text, nullable=True, comment="说明文字")
    description = Column(Text, nullable=True, comment="文件描述")
    seo_keywords = Column(String(500), nullable=True, comment="SEO关键词")

    # 上传和权限
    uploaded_by = Column(String(100), nullable=True, comment="上传者")
    is_public = Column(Boolean, default=True, comment="是否公开")

    # 统计信息
    usage_count = Column(Integer, default=0, nullable=False, comment="使用次数")
    download_count = Column(Integer, default=0, comment="下载次数")
    view_count = Column(Integer, default=0, comment="查看次数")

    # 关系
    folder = relationship("MediaFolder", back_populates="files")

    @property
    def file_url(self):
        """Get the file URL"""
        return self.path_original

    @property
    def is_image(self):
        """Check if file is an image"""
        return self.file_type == "image"

    @property
    def is_video(self):
        """Check if file is a video"""
        return self.file_type == "video"

    @property
    def is_document(self):
        """Check if file is a document"""
        return self.file_type == "document"

    @property
    def size_formatted(self):
        """Get formatted file size"""
        size = self.size_bytes
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
