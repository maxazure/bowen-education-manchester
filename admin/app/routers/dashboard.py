"""
管理后台仪表板路由

仪表板统计、快捷操作、最近活动等功能
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import (
    Post, Product, Gallery, ContactMessage,
    MediaFile, SiteColumn, AdminUser, Notification
)

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="admin/templates")


@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """
    管理后台仪表板

    显示统计信息、快捷操作、最近活动等
    """
    # 获取今日统计
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    stats = {
        # 文章统计
        "posts_total": db.query(func.count(Post.id)).scalar() or 0,
        "posts_today": db.query(func.count(Post.id)).filter(Post.created_at >= today).scalar() or 0,
        "posts_published": db.query(func.count(Post.id)).filter(Post.status == 'published').scalar() or 0,
        "posts_drafts": db.query(func.count(Post.id)).filter(Post.status == 'draft').scalar() or 0,

        # 产品统计
        "products_total": db.query(func.count(Product.id)).scalar() or 0,

        # 媒体统计
        "media_total": db.query(func.count(MediaFile.id)).scalar() or 0,
        "media_today": db.query(func.count(MediaFile.id)).filter(MediaFile.created_at >= today).scalar() or 0,

        # 相册统计
        "galleries_total": db.query(func.count(Gallery.id)).scalar() or 0,

        # 留言统计
        "contacts_total": db.query(func.count(ContactMessage.id)).scalar() or 0,
        "contacts_unread": db.query(func.count(ContactMessage.id)).filter(
            ContactMessage.status == 'unread'
        ).scalar() or 0,

        # 栏目统计
        "columns_total": db.query(func.count(SiteColumn.id)).scalar() or 0,

        # 用户统计
        "users_total": db.query(func.count(AdminUser.id)).scalar() or 0,
        "users_active": db.query(func.count(AdminUser.id)).filter(
            AdminUser.is_active == True
        ).scalar() or 0,
    }

    # 最近文章
    recent_posts = db.query(Post).order_by(desc(Post.created_at)).limit(5).all()

    # 最近留言
    recent_contacts = db.query(ContactMessage).order_by(
        desc(ContactMessage.created_at)
    ).limit(5).all()

    # 待办事项
    pending_tasks = []

    # 待审核的文章
    pending_posts = db.query(func.count(Post.id)).filter(
        Post.is_approved == 0
    ).scalar() or 0
    if pending_posts > 0:
        pending_tasks.append({
            "type": "post_approval",
            "icon": "bi-file-earmark-check",
            "color": "warning",
            "text": f"{pending_posts} 篇待审核文章",
            "link": "/admin/posts/pending-approval"
        })

    # 未读留言
    if stats["contacts_unread"] > 0:
        pending_tasks.append({
            "type": "unread_contacts",
            "icon": "bi-envelope",
            "color": "danger",
            "text": f"{stats['contacts_unread']} 条未读留言",
            "link": "/admin/contacts"
        })

    # 即将发布的内容
    scheduled_posts = db.query(Post).filter(
        Post.scheduled_at != None,
        Post.scheduled_at > datetime.now(),
        Post.status == 'scheduled'
    ).order_by(Post.scheduled_at).limit(3).all()
    if scheduled_posts:
        for post in scheduled_posts:
            pending_tasks.append({
                "type": "scheduled",
                "icon": "bi-clock",
                "color": "info",
                "text": f"'{post.title[:15]}...' 即将发布",
                "link": f"/admin/posts/{post.id}/edit"
            })

    # 系统通知
    notifications = db.query(Notification).filter(
        Notification.is_read == False,
        Notification.recipient_role.in_(['all', 'admin'])
    ).order_by(desc(Notification.created_at)).limit(5).all()

    recent_activities = []
    for notif in notifications:
        recent_activities.append({
            "type": "notification",
            "icon": f"bi-{notif.level}-circle",
            "color": notif.level,
            "text": notif.title,
            "time": notif.created_at,
            "link": notif.link
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats,
        "recent_posts": recent_posts,
        "recent_contacts": recent_contacts,
        "pending_tasks": pending_tasks,
        "recent_activities": recent_activities,
        "scheduled_posts": scheduled_posts,
    })


@router.get("/api/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取仪表板统计API"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    this_week_start = today - timedelta(days=today.weekday())
    this_month_start = today.replace(day=1)

    # 获取本周和本月数据
    posts_this_week = db.query(func.count(Post.id)).filter(
        Post.created_at >= this_week_start
    ).scalar() or 0
    posts_this_month = db.query(func.count(Post.id)).filter(
        Post.created_at >= this_month_start
    ).scalar() or 0

    # 文章趋势（最近7天）
    trend_data = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        next_date = date + timedelta(days=1)
        count = db.query(func.count(Post.id)).filter(
            Post.created_at >= date,
            Post.created_at < next_date
        ).scalar() or 0
        trend_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "label": f"{date.month}/{date.day}",
            "count": count
        })

    return JSONResponse(content={
        "success": True,
        "data": {
            "today": {
                "posts": db.query(func.count(Post.id)).filter(Post.created_at >= today).scalar() or 0,
                "media": db.query(func.count(MediaFile.id)).filter(MediaFile.created_at >= today).scalar() or 0,
                "contacts": db.query(func.count(ContactMessage.id)).filter(ContactMessage.created_at >= today).scalar() or 0,
            },
            "this_week": {"posts": posts_this_week},
            "this_month": {"posts": posts_this_month},
            "trend": trend_data,
        }
    })


@router.get("/api/quick-actions")
async def get_quick_actions(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取快捷操作列表"""
    actions = [
        {"id": "new_post", "icon": "bi-file-earmark-plus", "color": "primary", "label": "写文章", "link": "/admin/posts/new", "permission": "post:create"},
        {"id": "new_product", "icon": "bi-box-seam", "color": "success", "label": "添加产品", "link": "/admin/products/new", "permission": "product:create"},
        {"id": "upload_media", "icon": "bi-cloud-upload", "color": "info", "label": "上传媒体", "link": "/admin/media?upload=true", "permission": "media:upload"},
        {"id": "new_gallery", "icon": "bi-images", "color": "warning", "label": "创建相册", "link": "/admin/galleries/new", "permission": "gallery:create"},
        {"id": "view_contacts", "icon": "bi-chat-dots", "color": "danger", "label": "查看留言", "link": "/admin/contacts", "permission": "user:read"},
        {"id": "export_data", "icon": "bi-download", "color": "secondary", "label": "导出数据", "link": "/admin/export", "permission": "user:read"},
    ]

    # 根据权限过滤
    available_actions = [a for a in actions if admin_user.has_permission(a["permission"])]

    return JSONResponse(content={"success": True, "data": available_actions})


@router.get("/api/activity")
async def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取最近活动"""
    activities = []

    # 最近创建的文章
    posts = db.query(Post).order_by(desc(Post.created_at)).limit(limit).all()
    for post in posts:
        activities.append({
            "type": "post", "icon": "bi-file-earmark-text", "color": "primary",
            "text": f"创建文章: {post.title[:20]}...",
            "time": post.created_at.isoformat() if post.created_at else None,
            "link": f"/admin/posts/{post.id}/edit"
        })

    # 最近上传的媒体
    media = db.query(MediaFile).order_by(desc(MediaFile.created_at)).limit(limit).all()
    for m in media:
        activities.append({
            "type": "media", "icon": "bi-image", "color": "success",
            "text": f"上传媒体: {m.filename[:20]}",
            "time": m.created_at.isoformat() if m.created_at else None,
            "link": f"/admin/media"
        })

    # 新留言
    contacts = db.query(ContactMessage).order_by(desc(ContactMessage.created_at)).limit(limit).all()
    for c in contacts:
        activities.append({
            "type": "contact", "icon": "bi-envelope", "color": "warning",
            "text": f"新留言: {c.author_name[:15]}",
            "time": c.created_at.isoformat() if c.created_at else None,
            "link": f"/admin/contacts/{c.id}"
        })

    activities.sort(key=lambda x: x["time"] or "", reverse=True)
    return JSONResponse(content={"success": True, "data": activities[:limit]})
