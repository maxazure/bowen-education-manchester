"""Database models module"""

# 基础模型
from app.models.base import BaseModel

# 管理员模块
from app.models.admin_user import AdminUser

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

__all__ = [
    "AdminUser",
    "BaseModel",
    "ColumnType",
    "ContactMessage",
    "Event",
    "EventRegistration",
    "EventTicketType",
    "FAQ",
    "FAQCategory",
    "Gallery",
    "GalleryImage",
    "MediaFile",
    "MediaFolder",
    "MenuLocation",
    "Post",
    "PostCategory",
    "PostCategoryLink",
    "Product",
    "ProductCategory",
    "ProductCategoryLink",
    "SinglePage",
    "SiteColumn",
    "SiteSetting",
    "TeamMember",
]
