"""站点相关模型：栏目、单页、站点设置"""

import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class ColumnType(str, enum.Enum):
    """栏目类型枚举"""

    SINGLE_PAGE = "SINGLE_PAGE"  # 单页
    POST = "POST"  # 文章栏目
    PRODUCT = "PRODUCT"  # 产品栏目
    CUSTOM = "CUSTOM"  # 自定义模块


class MenuLocation(str, enum.Enum):
    """菜单位置枚举"""

    HEADER = "header"  # 顶部主菜单
    FOOTER = "footer"  # 底部菜单
    BOTH = "both"  # 同时显示在顶部和底部
    NONE = "none"  # 不显示在任何菜单（用于隐藏栏目）


class SiteColumn(BaseModel):
    """
    栏目/导航模型

    定义整站的栏目结构，用于前台导航和路由
    """

    __tablename__ = "site_column"

    name = Column(String(100), nullable=False, comment="栏目名称")
    slug = Column(String(100), unique=True, nullable=False, comment="URL Slug")
    column_type = Column(Enum(ColumnType), nullable=False, comment="栏目类型")
    parent_id = Column(
        Integer, ForeignKey("site_column.id"), nullable=True, comment="父栏目ID"
    )
    icon = Column(String(50), nullable=True, comment="图标标识")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    menu_location = Column(
        String(20),
        default="header",
        nullable=False,
        comment="菜单位置: header, footer, both, none"
    )
    show_in_nav = Column(
        Boolean, default=True, nullable=False, comment="是否显示在导航"
    )
    is_enabled = Column(Boolean, default=True, nullable=False, comment="是否启用")

    # 关系
    parent = relationship("SiteColumn", remote_side="SiteColumn.id", backref="children")


class SinglePage(BaseModel):
    """
    单页内容模型

    用于"关于我们"、"联系我们"等单页面内容
    """

    __tablename__ = "single_page"

    column_id = Column(
        Integer,
        ForeignKey("site_column.id"),
        unique=True,
        nullable=False,
        comment="关联栏目ID",
    )
    title = Column(String(200), nullable=False, comment="页面标题")
    subtitle = Column(String(300), nullable=True, comment="副标题")
    content_html = Column(Text, nullable=False, comment="页面内容HTML")
    hero_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="主图/背景图ID"
    )
    seo_title = Column(String(200), nullable=True, comment="SEO标题")
    seo_description = Column(Text, nullable=True, comment="SEO描述")
    status = Column(
        Enum("draft", "published", "hidden", name="single_page_status"),
        default="draft",
        nullable=False,
        comment="状态",
    )
    published_at = Column(DateTime, nullable=True, comment="发布时间")

    # 关系
    column = relationship("SiteColumn", backref="single_page")
    hero_media = relationship("MediaFile", foreign_keys=[hero_media_id])


class SiteSetting(BaseModel):
    """
    站点设置模型

    键值对配置，用于模板中的 site_info() 函数
    """

    __tablename__ = "site_setting"

    setting_key = Column(String(100), unique=True, nullable=False, comment="配置键")
    value_text = Column(Text, nullable=False, comment="配置值")
    value_type = Column(
        Enum("string", "html", "json", "media", name="setting_value_type"),
        default="string",
        nullable=False,
        comment="值类型",
    )
