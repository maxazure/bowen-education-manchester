"""
仪表板统计数据 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models import Post, Product, Gallery, ContactMessage

router = APIRouter(prefix="/api", tags=["dashboard-stats"])


@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    获取仪表板统计数据

    返回所有需要显示在仪表板上的统计信息
    """
    # 文章统计
    posts_count = db.query(Post).count()
    published_posts = db.query(Post).filter(Post.status == "published").count()
    draft_posts = db.query(Post).filter(Post.status == "draft").count()

    # 产品统计
    products_count = db.query(Product).count()

    # 相册统计
    galleries_count = db.query(Gallery).count()

    # 留言统计
    contacts_total = db.query(ContactMessage).count()
    unread_contacts = (
        db.query(ContactMessage).filter(ContactMessage.status == "unread").count()
    )
    handled_contacts = (
        db.query(ContactMessage).filter(ContactMessage.status == "handled").count()
    )

    # 媒体文件统计（从文件系统）
    import os
    media_dir = "templates/static/uploads"
    media_count = 0
    if os.path.exists(media_dir):
        for root, dirs, files in os.walk(media_dir):
            media_count += len([f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))])

    return {
        "success": True,
        "data": {
            # 统计卡片数据
            "posts": posts_count,
            "products": products_count,
            "galleries": galleries_count,
            "contacts": unread_contacts,  # 待处理 = 未读留言
            "contacts_total": contacts_total,
            "contacts_unread": unread_contacts,
            "contacts_handled": handled_contacts,
            "media": media_count,
            # 内容分布
            "published_posts": published_posts,
            "draft_posts": draft_posts,
        }
    }
