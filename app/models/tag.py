"""标签管理模型"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func

from app.database import Base
from app.models.base import BaseModel


class Tag(BaseModel):
    """
    标签模型

    用于对内容进行灵活分类和标记，不受栏目层级限制
    """

    __tablename__ = "tag"

    name = Column(String(50), nullable=False, comment="标签名称")
    name_en = Column(String(100), nullable=True, comment="标签英文名称")
    slug = Column(String(50), nullable=False, unique=True, comment="标签Slug")
    color = Column(String(7), default="#667eea", nullable=False, comment="标签颜色(HEX)")
    description = Column(Text, nullable=True, comment="标签描述")
    description_en = Column(Text, nullable=True, comment="标签英文描述")
    icon = Column(String(50), nullable=True, comment="标签图标")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")

    # 关系
    posts = relationship("Post", secondary="post_tag_link", back_populates="tags")

    @property
    def post_count(self):
        """获取使用此标签的文章数量"""
        return len(self.posts) if self.posts else 0


class PostTagLink(Base):
    """
    文章与标签的多对多关联表
    """

    __tablename__ = "post_tag_link"

    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True, comment="文章ID")
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True, comment="标签ID")
    created_at = Column(
        DateTime, default=func.now(), nullable=False, comment="关联创建时间"
    )
