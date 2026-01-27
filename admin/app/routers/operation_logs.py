"""
操作日志路由
"""

import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from admin.app.database import get_db
from app.models.operation_log import OperationLog
from admin.app.dependencies import get_current_admin_user

router = APIRouter(tags=["operation-log"])


@router.get("/operation-logs", response_class=HTMLResponse)
async def operation_logs_page(
    request: Request,
    action: Optional[str] = None,
    module: Optional[str] = None,
    admin_id: Optional[int] = None,
    page: int = 1,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """操作日志页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 查询条件
    query = db.query(OperationLog)

    if action:
        query = query.filter(OperationLog.action == action)
    if module:
        query = query.filter(OperationLog.module == module)
    if admin_id:
        query = query.filter(OperationLog.admin_user_id == admin_id)

    # 分页
    per_page = 50
    total = query.count()
    logs = (
        query
        .order_by(desc(OperationLog.created_at))
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    # 统计信息
    stats = {
        "total": db.query(OperationLog).count(),
        "today": db.query(OperationLog).filter(
            OperationLog.created_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count(),
        "this_week": db.query(OperationLog).filter(
            OperationLog.created_at >= datetime.now() - timedelta(days=7)
        ).count(),
        "this_month": db.query(OperationLog).filter(
            OperationLog.created_at >= datetime.now() - timedelta(days=30)
        ).count(),
    }

    # 获取筛选选项
    action_options = (
        db.query(OperationLog.action)
        .distinct()
        .all()
    )
    module_options = (
        db.query(OperationLog.module)
        .distinct()
        .all()
    )

    return templates.TemplateResponse("operation_logs.html", {
        "request": request,
        "logs": logs,
        "stats": stats,
        "action_options": [a[0] for a in action_options],
        "module_options": [m[0] for m in module_options],
        "current_action": action,
        "current_module": module,
        "current_admin": admin_id,
        "page": page,
        "total": total,
        "per_page": per_page,
    })


@router.get("/api/operation-logs")
async def get_operation_logs(
    action: Optional[str] = None,
    module: Optional[str] = None,
    admin_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取操作日志列表API"""
    query = db.query(OperationLog)

    if action:
        query = query.filter(OperationLog.action == action)
    if module:
        query = query.filter(OperationLog.module == module)
    if admin_id:
        query = query.filter(OperationLog.admin_user_id == admin_id)
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(OperationLog.created_at >= start)
        except ValueError:
            pass
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(OperationLog.created_at <= end)
        except ValueError:
            pass

    total = query.count()
    logs = (
        query
        .order_by(desc(OperationLog.created_at))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return JSONResponse(content={
        "success": True,
        "data": {
            "logs": [
                {
                    "id": log.id,
                    "admin_username": log.admin_username,
                    "action": log.action,
                    "module": log.module,
                    "target_type": log.target_type,
                    "target_id": log.target_id,
                    "target_name": log.target_name,
                    "description": log.description,
                    "ip_address": log.ip_address,
                    "status": log.status,
                    "created_at": log.created_at.isoformat(),
                }
                for log in logs
            ],
            "total": total,
            "page": page,
            "limit": limit,
        }
    })


@router.get("/api/operation-logs/stats")
async def get_operation_stats(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取操作统计"""
    since = datetime.now() - timedelta(days=days)

    # 按action统计
    action_stats = (
        db.query(
            OperationLog.action,
            db.func.count(OperationLog.id).label("count")
        )
        .filter(OperationLog.created_at >= since)
        .group_by(OperationLog.action)
        .all()
    )

    # 按module统计
    module_stats = (
        db.query(
            OperationLog.module,
            db.func.count(OperationLog.id).label("count")
        )
        .filter(OperationLog.created_at >= since)
        .group_by(OperationLog.module)
        .all()
    )

    # 最近活动
    recent_logs = (
        db.query(OperationLog)
        .order_by(desc(OperationLog.created_at))
        .limit(10)
        .all()
    )

    return JSONResponse(content={
        "success": True,
        "data": {
            "action_stats": [{"action": a, "count": c} for a, c in action_stats],
            "module_stats": [{"module": m, "count": c} for m, c in module_stats],
            "recent_activity": [
                {
                    "id": log.id,
                    "action": log.action,
                    "module": log.module,
                    "description": log.description,
                    "admin_username": log.admin_username,
                    "created_at": log.created_at.isoformat(),
                }
                for log in recent_logs
            ],
            "total_logs": db.query(OperationLog).filter(OperationLog.created_at >= since).count(),
        }
    })


@router.post("/api/operation-logs")
async def create_log(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """记录操作日志"""
    from pydantic import BaseModel

    class LogCreate(BaseModel):
        action: str
        module: str
        target_type: Optional[str] = None
        target_id: Optional[int] = None
        target_name: Optional[str] = None
        description: Optional[str] = None
        old_data: Optional[dict] = None
        new_data: Optional[dict] = None
        status: str = "success"
        error_message: Optional[str] = None

    data = await request.json()
    log_data = LogCreate(**data)

    # 获取客户端IP
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent", "")[:500]

    log = OperationLog(
        admin_user_id=admin_user.id if admin_user else None,
        admin_username=admin_user.username if admin_user else None,
        action=log_data.action,
        module=log_data.module,
        target_type=log_data.target_type,
        target_id=log_data.target_id,
        target_name=log_data.target_name,
        description=log_data.description,
        old_data=log_data.old_data,
        new_data=log_data.new_data,
        ip_address=client_ip,
        user_agent=user_agent,
        status=log_data.status,
        error_message=log_data.error_message,
    )
    db.add(log)
    db.commit()

    return JSONResponse(content={"success": True, "log_id": log.id})


@router.delete("/api/operation-logs/cleanup")
async def cleanup_logs(
    days: int = Query(90, ge=30, le=365),
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """清理旧日志"""
    cutoff_date = datetime.now() - timedelta(days=days)
    deleted = (
        db.query(OperationLog)
        .filter(OperationLog.created_at < cutoff_date)
        .delete()
    )
    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": f"已删除 {deleted} 条超过 {days} 天的日志"
    })
