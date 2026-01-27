"""内容版本历史模型"""

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import BaseModel


class ContentVersion(BaseModel):
    """
    内容版本历史模型

    记录文章、产品等内容的修改历史，支持版本回滚
    """

    __tablename__ = "content_version"

    # 内容类型: post=文章, product=产品
    content_type = Column(String(20), nullable=False, comment="内容类型")
    content_id = Column(Integer, nullable=False, comment="内容ID")

    # 版本信息
    version_number = Column(Integer, nullable=False, default=1, comment="版本号")
    title = Column(String(200), nullable=True, comment="当时的标题")
    content_snapshot = Column(Text, nullable=True, comment="内容快照(JSON格式)")

    # 操作信息
    action = Column(String(20), nullable=False, comment="操作类型: create/update/publish")
    admin_id = Column(Integer, nullable=True, comment="管理员ID")
    admin_name = Column(String(100), nullable=True, comment="管理员名称")

    # 备注
    remark = Column(String(500), nullable=True, comment="修改备注")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "content_type": self.content_type,
            "content_id": self.content_id,
            "version_number": self.version_number,
            "title": self.title,
            "content_snapshot": self.content_snapshot,
            "action": self.action,
            "admin_id": self.admin_id,
            "admin_name": self.admin_name,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
