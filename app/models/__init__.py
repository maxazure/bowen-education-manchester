"""Database models module"""

# 基础模型
from app.models.base import BaseModel

# 管理员模块
from app.models.admin_user import AdminUser, Role, UserRole, PERMISSIONS

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
    MediaFolder,
)
from app.models.contact import (
    ContactMessage,
)

# 基础内容模块
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

# 活动模块
from app.models.event import (
    Event,
    EventRegistration,
    EventTicketType,
)

# 多媒体模块
from app.models.gallery import (
    Gallery,
    GalleryImage,
)

# Hero幻灯片模块
from app.models.hero import (
    HeroSlide,
)

# 版本历史模块
from app.models.content_version import (
    ContentVersion,
)

# 通知模块
from app.models.notification import (
    Notification,
)

# 评论模块
from app.models.comment import (
    Comment,
)

# 标签模块
from app.models.tag import (
    Tag,
    PostTagLink,
)

# 访问统计模块
from app.models.visit import (
    PageVisit,
    VisitLog,
    VisitSummary,
)

__all__ = [
    "AdminUser",
    "BaseModel",
    "ColumnType",
    "Comment",
    "ContactMessage",
    "ContentVersion",
    "Notification",
    "Event",
    "EventRegistration",
    "EventTicketType",
    "FAQ",
    "FAQCategory",
    "Gallery",
    "GalleryImage",
    "HeroSlide",
    "MediaFile",
    "MediaFolder",
    "MenuLocation",
    "PageVisit",
    "PERMISSIONS",
    "Post",
    "PostCategory",
    "PostCategoryLink",
    "PostTagLink",
    "Product",
    "ProductCategory",
    "ProductCategoryLink",
    "Role",
    "SinglePage",
    "SiteColumn",
    "SiteSetting",
    "Tag",
    "TeamMember",
    "UserRole",
    "VisitLog",
    "VisitSummary",
]
