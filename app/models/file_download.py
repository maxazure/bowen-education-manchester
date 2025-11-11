"""文件下载模块 - File Download Module"""

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class FileCategory(BaseModel):
    """
    文件分类模型

    用于组织文档与资源,如产品手册、报告、表格、软件等
    """

    __tablename__ = "file_category"

    # 基本信息
    name = Column(String(100), nullable=False, comment="分类名称")
    slug = Column(String(100), nullable=False, comment="分类Slug")
    description = Column(Text, nullable=True, comment="分类描述")

    # 层级结构
    parent_id = Column(
        Integer, ForeignKey("file_category.id"), nullable=True, comment="父分类ID"
    )

    # 图标
    icon_class = Column(String(50), nullable=True, comment="图标CSS类名")

    # 显示控制
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_visible = Column(Boolean, default=True, nullable=False, comment="是否可见")

    # 关系
    parent = relationship(
        "FileCategory", remote_side="FileCategory.id", backref="children"
    )

    def __repr__(self):
        return f"<FileCategory {self.name}>"


class FileDownload(BaseModel):
    """
    文件下载模型

    管理可下载的文档与资源,支持权限控制、版本管理、下载统计
    """

    __tablename__ = "file_download"

    # 基本信息
    title = Column(String(200), nullable=False, comment="文件标题")
    slug = Column(String(200), nullable=False, comment="文件Slug")
    description = Column(Text, nullable=True, comment="文件描述")

    # 分类
    category_id = Column(
        Integer, ForeignKey("file_category.id"), nullable=True, comment="文件分类ID"
    )

    # 文件信息
    file_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=False, comment="文件ID"
    )
    file_name = Column(String(255), nullable=False, comment="文件名")
    file_extension = Column(String(20), nullable=True, comment="文件扩展名")
    file_size_kb = Column(Integer, nullable=True, comment="文件大小(KB)")
    file_type = Column(
        Enum(
            "pdf",
            "doc",
            "xls",
            "ppt",
            "zip",
            "image",
            "video",
            "other",
            name="file_download_type",
        ),
        default="other",
        nullable=False,
        comment="文件类型",
    )

    # 版本管理
    version = Column(String(50), nullable=True, comment="文件版本号")
    is_latest = Column(Boolean, default=True, nullable=False, comment="是否为最新版本")
    previous_version_id = Column(
        Integer, ForeignKey("file_download.id"), nullable=True, comment="前一版本ID"
    )

    # 缩略图/预览图
    thumbnail_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="缩略图ID"
    )

    # 访问控制
    access_level = Column(
        Enum("public", "members_only", "vip_only", "admin_only", name="file_access_level"),
        default="public",
        nullable=False,
        comment="访问权限",
    )
    requires_login = Column(
        Boolean, default=False, nullable=False, comment="是否需要登录下载"
    )
    allowed_roles = Column(
        String(255), nullable=True, comment="允许下载的角色(逗号分隔)"
    )

    # 下载限制
    download_limit_per_user = Column(
        Integer, nullable=True, comment="每个用户下载次数限制(null表示不限)"
    )
    link_expiry_days = Column(
        Integer, nullable=True, comment="下载链接有效期(天,null表示永久)"
    )

    # 显示控制
    is_featured = Column(Boolean, default=False, nullable=False, comment="是否推荐")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")
    status = Column(
        Enum("draft", "published", "archived", name="file_status"),
        default="draft",
        nullable=False,
        comment="文件状态",
    )
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")

    # 标签
    tags = Column(String(255), nullable=True, comment="标签(逗号分隔)")

    # 统计
    download_count = Column(Integer, default=0, nullable=False, comment="下载次数")
    view_count = Column(Integer, default=0, nullable=False, comment="查看次数")
    last_downloaded_at = Column(DateTime, nullable=True, comment="最后下载时间")

    # 文件说明
    usage_instructions = Column(Text, nullable=True, comment="使用说明")
    system_requirements = Column(Text, nullable=True, comment="系统要求")
    release_notes = Column(Text, nullable=True, comment="发布说明/更新日志")

    # SEO
    seo_title = Column(String(200), nullable=True, comment="SEO标题")
    seo_description = Column(Text, nullable=True, comment="SEO描述")

    # 其他
    author = Column(String(100), nullable=True, comment="作者")
    published_date = Column(DateTime, nullable=True, comment="发布日期")
    last_updated_date = Column(DateTime, nullable=True, comment="最后更新日期")
    notes = Column(Text, nullable=True, comment="内部备注")

    # 关系
    category = relationship("FileCategory", backref="files")
    file_media = relationship("MediaFile", foreign_keys=[file_media_id])
    thumbnail_media = relationship("MediaFile", foreign_keys=[thumbnail_media_id])
    previous_version = relationship(
        "FileDownload", remote_side="FileDownload.id", backref="newer_versions"
    )
    download_logs = relationship(
        "FileDownloadLog", back_populates="file", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<FileDownload {self.title}>"


class FileDownloadLog(BaseModel):
    """
    文件下载日志模型

    记录文件下载历史,用于统计和审计
    """

    __tablename__ = "file_download_log"

    # 关联信息
    file_id = Column(
        Integer, ForeignKey("file_download.id"), nullable=False, comment="文件ID"
    )
    user_id = Column(
        Integer, ForeignKey("user.id"), nullable=True, comment="用户ID(已登录用户)"
    )

    # 下载信息
    ip_address = Column(String(50), nullable=True, comment="下载IP地址")
    user_agent = Column(String(500), nullable=True, comment="用户代理")
    referrer = Column(String(500), nullable=True, comment="来源页面")

    # 下载状态
    download_status = Column(
        Enum("success", "failed", "cancelled", name="download_log_status"),
        default="success",
        nullable=False,
        comment="下载状态",
    )
    error_message = Column(Text, nullable=True, comment="错误信息(如果失败)")

    # 其他
    downloaded_at = Column(DateTime, nullable=True, comment="下载时间")

    # 关系
    file = relationship("FileDownload", back_populates="download_logs")
    user = relationship("User", backref="file_downloads")

    def __repr__(self):
        return f"<FileDownloadLog file_id={self.file_id} user_id={self.user_id}>"
