"""回收站模型 - 用于软删除功能"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base
from app.models.base import BaseModel


class TrashItem(BaseModel):
    """
    回收站项目模型

    用于存储软删除的内容，支持恢复和彻底删除
    """
    __tablename__ = "trash_item"

    # 内容类型: post, product, gallery, column, page, media
    content_type = Column(String(50), nullable=False, comment="内容类型")
    content_id = Column(Integer, nullable=False, comment="原始内容ID")

    # 存储原始数据的JSON
    original_data = Column(Text, nullable=False, comment="原始数据JSON")

    # 删除信息
    deleted_at = Column(DateTime, nullable=False, comment="删除时间")
    deleted_by = Column(Integer, nullable=True, comment="删除人ID")
    delete_reason = Column(String(500), nullable=True, comment="删除原因")

    # 统计信息
    storage_size = Column(Integer, default=0, nullable=False, comment="存储大小(字节)")

    def __repr__(self):
        return f"<TrashItem {self.content_type}:{self.content_id}>"
