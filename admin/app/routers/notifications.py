"""
通知管理路由
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models import Notification, ContactMessage

router = APIRouter(tags=["notifications"])


@router.get("/notifications")
async def get_notifications(
    unread_only: bool = Query(False, description="仅获取未读通知"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """获取通知列表"""
    query = db.query(Notification).filter(Notification.recipient_role == "admin")

    if unread_only:
        query = query.filter(Notification.is_read == False)

    # 获取未读通知数量
    unread_count = db.query(Notification).filter(
        Notification.recipient_role == "admin",
        Notification.is_read == False
    ).count()

    # 获取最近留言数量（用于显示新留言提醒）
    recent_contacts = db.query(ContactMessage).filter(
        ContactMessage.status == "unread"
    ).count()

    notifications = query.order_by(
        Notification.created_at.desc()
    ).limit(limit).all()

    return JSONResponse(content={
        "success": True,
        "data": {
            "notifications": [n.to_dict() for n in notifications],
            "unread_count": unread_count,
            "recent_contacts": recent_contacts,
        }
    })


@router.post("/notifications/mark-read/{notification_id}")
async def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
):
    """标记通知为已读"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        return JSONResponse(
            content={"success": False, "message": "通知不存在"},
            status_code=404
        )

    notification.is_read = True
    notification.read_at = datetime.now()
    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": "已标记为已读"
    })


@router.post("/notifications/mark-all-read")
async def mark_all_notifications_read(
    db: Session = Depends(get_db),
):
    """标记所有通知为已读"""
    db.query(Notification).filter(
        Notification.recipient_role == "admin",
        Notification.is_read == False
    ).update({
        "is_read": True,
        "read_at": datetime.now()
    })
    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": "已全部标记为已读"
    })


@router.delete("/notifications/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    """删除通知"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        return JSONResponse(
            content={"success": False, "message": "通知不存在"},
            status_code=404
        )

    db.delete(notification)
    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": "已删除通知"
    })


@router.post("/notifications/create")
async def create_notification(
    type: str = "system",
    level: str = "info",
    title: str = "",
    content: str = "",
    link: Optional[str] = None,
    link_text: Optional[str] = None,
    recipient_role: str = "admin",
    db: Session = Depends(get_db),
):
    """创建新通知"""
    notification = Notification(
        type=type,
        level=level,
        title=title,
        content=content,
        link=link,
        link_text=link_text,
        recipient_role=recipient_role,
        is_read=False,
    )

    db.add(notification)
    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": "通知已创建",
        "data": notification.to_dict()
    })


@router.get("/notifications/stats")
async def get_notification_stats(
    db: Session = Depends(get_db),
):
    """获取通知统计"""
    # 未读通知数
    unread = db.query(Notification).filter(
        Notification.recipient_role == "admin",
        Notification.is_read == False
    ).count()

    # 未处理留言数
    unread_contacts = db.query(ContactMessage).filter(
        ContactMessage.status == "unread"
    ).count()

    # 按类型统计
    by_type = {}
    for type_val, type_name in Notification.TYPE_CHOICES:
        count = db.query(Notification).filter(
            Notification.recipient_role == "admin",
            Notification.type == type_val,
            Notification.is_read == False
        ).count()
        if count > 0:
            by_type[type_val] = {"name": type_name, "count": count}

    return JSONResponse(content={
        "success": True,
        "data": {
            "unread_notifications": unread,
            "unread_contacts": unread_contacts,
            "total_unread": unread + unread_contacts,
            "by_type": by_type,
        }
    })
