"""常见问题模块 - FAQ Module"""

from sqlalchemy import Boolean, Column, Integer, String, Text

from app.models.base import BaseModel


class FAQ(BaseModel):
    """
    常见问题模型

    用于展示FAQ（常见问题与答案）
    """

    __tablename__ = "faq"

    category = Column(String(100), nullable=True, comment="问题分类")
    question = Column(String(500), nullable=False, comment="问题")
    answer = Column(Text, nullable=False, comment="答案")

    # 展示控制
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_visible = Column(Boolean, default=True, nullable=False, comment="是否可见")
    is_pinned = Column(Boolean, default=False, nullable=False, comment="是否置顶")

    # 统计
    view_count = Column(Integer, default=0, nullable=False, comment="查看次数")
    helpful_count = Column(Integer, default=0, nullable=False, comment="有用次数")
    unhelpful_count = Column(Integer, default=0, nullable=False, comment="无用次数")


class FAQCategory(BaseModel):
    """
    FAQ分类模型
    """

    __tablename__ = "faq_category"

    name = Column(String(100), nullable=False, comment="分类名称")
    slug = Column(String(100), unique=True, nullable=False, comment="分类Slug")
    description = Column(Text, nullable=True, comment="分类描述")
    icon = Column(String(50), nullable=True, comment="图标标识")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_visible = Column(Boolean, default=True, nullable=False, comment="是否可见")
