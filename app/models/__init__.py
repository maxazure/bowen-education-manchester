"""Database models module"""

# 基础模型
from app.models.base import BaseModel

# 站点核心模块
from app.models.site import (
    SiteColumn,
    ColumnType,
    MenuLocation,
    SinglePage,
    SiteSetting,
)
from app.models.media import (
    MediaFile,
)
from app.models.base import (
    BaseModel,
)
from app.models.contact import (
    ContactMessage,
)

# 基础内容模块
from app.models.custom_field import (
    CustomFieldDef,
    CustomFieldOption,
    ProductCustomFieldValue,
)
from app.models.product import (
    Product,
    ProductCategory,
    ProductCategoryLink,
)
from app.models.post import (
    Post,
    PostCategory,
    PostCategoryLink,
)
from app.models.team import (
    TeamMember,
)
from app.models.faq import (
    FAQ,
    FAQCategory,
)

# 交互功能模块
from app.models.user import (
    User,
)

# 预约与服务模块
from app.models.booking import (
    Booking,
    BookingService,
    BookingTimeSlot,
)
from app.models.event import (
    Event,
    EventRegistration,
    EventTicketType,
)

# 多媒体与资源模块
from app.models.file_download import (
    FileCategory,
    FileDownload,
    FileDownloadLog,
)
from app.models.video import (
    Video,
    VideoCategory,
    VideoPlaylist,
    VideoPlaylistLink,
)
from app.models.gallery import (
    Gallery,
    GalleryImage,
)

__all__ = [
    "BaseModel",
    "BaseModel",
    "Booking",
    "BookingService",
    "BookingTimeSlot",
    "ColumnType",
    "ContactMessage",
    "MenuLocation",
    "CustomFieldDef",
    "CustomFieldOption",
    "Event",
    "EventRegistration",
    "EventTicketType",
    "FAQ",
    "FAQCategory",
    "FileCategory",
    "FileDownload",
    "FileDownloadLog",
    "Gallery",
    "GalleryImage",
    "MediaFile",
    "Post",
    "PostCategory",
    "PostCategoryLink",
    "Product",
    "ProductCategory",
    "ProductCategoryLink",
    "ProductCustomFieldValue",
    "SinglePage",
    "SiteColumn",
    "SiteSetting",
    "TeamMember",
    "User",
    "Video",
    "VideoCategory",
    "VideoPlaylist",
    "VideoPlaylistLink",
]
