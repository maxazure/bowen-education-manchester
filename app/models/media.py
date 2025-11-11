"""媒体文件模型"""

from sqlalchemy import Column, Integer, String

from app.models.base import BaseModel


class MediaFile(BaseModel):
    """
    媒体文件模型

    统一管理上传的图片和文件
    """

    __tablename__ = "media_file"

    filename_original = Column(String(255), nullable=False, comment="原始文件名")
    mime_type = Column(String(100), nullable=False, comment="MIME类型")
    size_bytes = Column(Integer, nullable=False, comment="文件大小（字节）")
    width = Column(Integer, nullable=True, comment="图片宽度")
    height = Column(Integer, nullable=True, comment="图片高度")
    path_original = Column(String(500), nullable=False, comment="原图路径")
    path_medium = Column(String(500), nullable=True, comment="中等尺寸图路径")
    path_thumb = Column(String(500), nullable=True, comment="缩略图路径")

    @property
    def file_url(self):
        """Get the file URL"""
        return self.path_original
