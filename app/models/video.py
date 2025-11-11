"""视频展示模块 - Video Gallery Module"""

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class VideoCategory(BaseModel):
    """
    视频分类模型

    用于组织视频内容,如企业宣传、教学视频、产品演示等
    """

    __tablename__ = "video_category"

    # 基本信息
    name = Column(String(100), nullable=False, comment="分类名称")
    slug = Column(String(100), nullable=False, comment="分类Slug")
    description = Column(Text, nullable=True, comment="分类描述")

    # 层级结构
    parent_id = Column(
        Integer, ForeignKey("video_category.id"), nullable=True, comment="父分类ID"
    )

    # 显示控制
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_visible = Column(Boolean, default=True, nullable=False, comment="是否可见")

    # 关系
    parent = relationship(
        "VideoCategory", remote_side="VideoCategory.id", backref="children"
    )

    def __repr__(self):
        return f"<VideoCategory {self.name}>"


class Video(BaseModel):
    """
    视频模型

    用于展示企业宣传片、教学视频、产品演示、活动记录等视频内容
    """

    __tablename__ = "video"

    # 基本信息
    title = Column(String(200), nullable=False, comment="视频标题")
    slug = Column(String(200), nullable=False, comment="视频Slug")
    description = Column(Text, nullable=True, comment="视频描述")

    # 分类
    category_id = Column(
        Integer, ForeignKey("video_category.id"), nullable=True, comment="视频分类ID"
    )

    # 视频源
    video_source = Column(
        Enum("upload", "youtube", "vimeo", "external", name="video_source"),
        default="upload",
        nullable=False,
        comment="视频来源",
    )
    video_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="上传视频文件ID"
    )
    youtube_id = Column(String(100), nullable=True, comment="YouTube视频ID")
    vimeo_id = Column(String(100), nullable=True, comment="Vimeo视频ID")
    external_url = Column(String(500), nullable=True, comment="外部视频链接")

    # 缩略图
    thumbnail_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="缩略图ID"
    )

    # 视频信息
    duration_seconds = Column(Integer, nullable=True, comment="视频时长(秒)")
    resolution = Column(String(20), nullable=True, comment="分辨率(如:1920x1080)")
    file_size_mb = Column(Integer, nullable=True, comment="文件大小(MB)")

    # 播放器设置
    autoplay = Column(Boolean, default=False, nullable=False, comment="是否自动播放")
    loop = Column(Boolean, default=False, nullable=False, comment="是否循环播放")
    muted = Column(Boolean, default=False, nullable=False, comment="是否静音")
    controls = Column(Boolean, default=True, nullable=False, comment="是否显示控制条")

    # 字幕
    has_subtitles = Column(Boolean, default=False, nullable=False, comment="是否有字幕")
    subtitle_url = Column(String(500), nullable=True, comment="字幕文件URL")

    # 显示控制
    is_featured = Column(Boolean, default=False, nullable=False, comment="是否推荐")
    is_public = Column(Boolean, default=True, nullable=False, comment="是否公开")
    status = Column(
        Enum("draft", "published", "archived", name="video_status"),
        default="draft",
        nullable=False,
        comment="视频状态",
    )
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")

    # 标签
    tags = Column(String(255), nullable=True, comment="标签(逗号分隔)")

    # 统计
    view_count = Column(Integer, default=0, nullable=False, comment="播放次数")
    like_count = Column(Integer, default=0, nullable=False, comment="点赞数")
    share_count = Column(Integer, default=0, nullable=False, comment="分享数")

    # SEO
    seo_title = Column(String(200), nullable=True, comment="SEO标题")
    seo_description = Column(Text, nullable=True, comment="SEO描述")

    # 嵌入代码
    embed_code = Column(Text, nullable=True, comment="嵌入代码")
    allow_embed = Column(
        Boolean, default=True, nullable=False, comment="是否允许嵌入"
    )

    # 访问控制
    requires_login = Column(
        Boolean, default=False, nullable=False, comment="是否需要登录观看"
    )
    allowed_roles = Column(
        String(255), nullable=True, comment="允许观看的角色(逗号分隔)"
    )

    # 其他
    notes = Column(Text, nullable=True, comment="备注")
    published_at = Column(String(200), nullable=True, comment="发布时间")

    # 关系
    category = relationship("VideoCategory", backref="videos")
    video_media = relationship("MediaFile", foreign_keys=[video_media_id])
    thumbnail_media = relationship("MediaFile", foreign_keys=[thumbnail_media_id])

    def __repr__(self):
        return f"<Video {self.title}>"


class VideoPlaylist(BaseModel):
    """
    视频播放列表模型

    用于组织相关视频成系列或课程
    """

    __tablename__ = "video_playlist"

    # 基本信息
    title = Column(String(200), nullable=False, comment="播放列表标题")
    slug = Column(String(200), nullable=False, comment="播放列表Slug")
    description = Column(Text, nullable=True, comment="播放列表描述")

    # 封面
    cover_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="封面图片ID"
    )

    # 显示控制
    is_featured = Column(Boolean, default=False, nullable=False, comment="是否推荐")
    is_public = Column(Boolean, default=True, nullable=False, comment="是否公开")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")

    # 统计
    video_count = Column(Integer, default=0, nullable=False, comment="视频数量")
    total_duration_seconds = Column(Integer, default=0, nullable=False, comment="总时长(秒)")

    # 其他
    notes = Column(Text, nullable=True, comment="备注")

    # 关系
    cover_media = relationship("MediaFile", foreign_keys=[cover_media_id])
    videos = relationship(
        "Video", secondary="video_playlist_link", backref="playlists"
    )

    def __repr__(self):
        return f"<VideoPlaylist {self.title}>"


class VideoPlaylistLink(BaseModel):
    """
    视频与播放列表的多对多关联表
    """

    __tablename__ = "video_playlist_link"

    # 关联
    playlist_id = Column(
        Integer, ForeignKey("video_playlist.id"), nullable=False, comment="播放列表ID"
    )
    video_id = Column(Integer, ForeignKey("video.id"), nullable=False, comment="视频ID")

    # 排序
    sort_order = Column(Integer, default=0, nullable=False, comment="在播放列表中的排序")

    def __repr__(self):
        return f"<VideoPlaylistLink playlist_id={self.playlist_id} video_id={self.video_id}>"
