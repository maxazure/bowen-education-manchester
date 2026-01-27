"""评论模型"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import BaseModel


class Comment(BaseModel):
    """
    评论模型

    用于文章、产品等的评论功能
    """

    __tablename__ = "comment"

    # 评论类型
    TYPE_CHOICES = [
        ("post", "文章评论"),
        ("product", "产品评论"),
    ]

    # 状态
    STATUS_CHOICES = [
        ("pending", "待审核"),
        ("approved", "已通过"),
        ("rejected", "已拒绝"),
        ("spam", "垃圾评论"),
    ]

    content_type = Column(String(20), nullable=False, comment="内容类型")
    content_id = Column(Integer, nullable=False, comment="内容ID")

    # 评论者信息
    author_name = Column(String(100), nullable=False, comment="评论者名称")
    author_email = Column(String(200), nullable=True, comment="评论者邮箱")
    author_ip = Column(String(45), nullable=True, comment="IP地址")
    user_agent = Column(String(500), nullable=True, comment="浏览器信息")

    # 评论内容
    content = Column(Text, nullable=False, comment="评论内容")

    # 状态
    status = Column(String(20), default="pending", nullable=False, comment="状态")

    # 父评论（回复）
    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True, comment="父评论ID")

    # 审核信息
    reviewed_by = Column(Integer, nullable=True, comment="审核人ID")
    reviewed_at = Column(DateTime, nullable=True, comment="审核时间")
    reply_content = Column(Text, nullable=True, comment="回复内容")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "content_type": self.content_type,
            "content_id": self.content_id,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "content": self.content,
            "status": self.status,
            "parent_id": self.parent_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
