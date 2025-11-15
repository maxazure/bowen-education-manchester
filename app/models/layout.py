"""页面布局模型：统一用于首页与自定义栏目页面的区块化编辑"""

import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class LayoutScope(str, enum.Enum):
    """布局作用域"""

    HOME = "home"
    COLUMN = "column"


class PageLayout(BaseModel):
    """页面布局实体

    用于承载某个页面（首页或栏目页）的区块化布局草稿与发布信息
    """

    __tablename__ = "page_layout"

    scope = Column(Enum(LayoutScope), nullable=False, comment="布局作用域：home 或 column")
    scope_id = Column(Integer, ForeignKey("site_column.id"), nullable=True, comment="作用域实体ID：首页为空，栏目为 site_column.id")
    status = Column(
        Enum("draft", "published", name="page_layout_status"),
        default="draft",
        nullable=False,
        comment="布局状态",
    )
    published_at = Column(DateTime, nullable=True, comment="发布时间")

    # 关系
    sections = relationship("PageLayoutSection", backref="layout", cascade="all, delete-orphan")


class PageLayoutSection(BaseModel):
    """布局中的分区（Section）"""

    __tablename__ = "page_layout_section"

    layout_id = Column(Integer, ForeignKey("page_layout.id"), nullable=False, comment="所属布局ID")
    title = Column(String(200), nullable=True, comment="分区标题")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_enabled = Column(Boolean, default=True, nullable=False, comment="是否启用")

    # 关系
    blocks = relationship("PageLayoutBlock", backref="section", cascade="all, delete-orphan")


class PageLayoutBlock(BaseModel):
    """布局中的区块实例"""

    __tablename__ = "page_layout_block"

    section_id = Column(Integer, ForeignKey("page_layout_section.id"), nullable=False, comment="所属分区ID")
    block_type = Column(String(100), nullable=False, comment="区块类型标识")
    attributes_json = Column(Text, nullable=True, comment="区块属性JSON")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_enabled = Column(Boolean, default=True, nullable=False, comment="是否启用")