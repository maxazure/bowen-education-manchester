"""通知模型"""

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import BaseModel


class Notification(BaseModel):
    """
    通知模型

    用于系统通知、内容更新提醒等
    """

    __tablename__ = "notification"

    # 通知类型
    TYPE_CHOICES = [
        ("system", "系统通知"),
        ("contact", "留言通知"),
        ("comment", "评论通知"),
        ("content", "内容更新"),
        ("warning", "警告"),
    ]

    # 通知级别
    LEVEL_CHOICES = [
        ("info", "信息"),
        ("success", "成功"),
        ("warning", "警告"),
        ("danger", "危险"),
    ]

    type = Column(String(20), default="system", nullable=False, comment="通知类型")
    level = Column(String(20), default="info", nullable=False, comment="通知级别")
    title = Column(String(200), nullable=False, comment="通知标题")
    content = Column(Text, nullable=True, comment="通知内容")

    # 链接
    link = Column(String(500), nullable=True, comment="跳转链接")
    link_text = Column(String(100), nullable=True, comment="链接文本")

    # 状态
    is_read = Column(Boolean, default=False, nullable=False, comment="是否已读")
    read_at = Column(DateTime, nullable=True, comment="阅读时间")

    # 接收者
    recipient_id = Column(Integer, nullable=True, comment="接收用户ID")
    recipient_role = Column(String(50), default="admin", nullable=False, comment="接收角色")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "type": self.type,
            "level": self.level,
            "title": self.title,
            "content": self.content,
            "link": self.link,
            "link_text": self.link_text,
            "is_read": self.is_read,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
