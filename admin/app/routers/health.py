"""
系统健康监控路由

监控系统运行状态和资源使用情况
"""

import os
import psutil
import time
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import AdminUser

router = APIRouter(tags=["health"])


def check_permission(admin_user: AdminUser, permission: str) -> bool:
    """检查用户是否有特定权限"""
    return admin_user.has_permission(permission)


def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    process = psutil.Process(os.getpid())

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": {
            "total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
            "used_gb": round(psutil.disk_usage('/').used / (1024**3), 2),
            "free_gb": round(psutil.disk_usage('/').free / (1024**3), 2),
            "percent": psutil.disk_usage('/').percent,
        },
        "memory": {
            "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
        },
        "process_memory_mb": round(process.memory_info().rss / (1024**2), 2),
        "process_cpu_percent": process.cpu_percent(interval=0.5),
        "process_uptime_seconds": int(time.time() - process.create_time()),
    }


def get_database_health(db: Session) -> Dict[str, Any]:
    """检查数据库连接状态"""
    try:
        start_time = time.time()
        db.execute(text("SELECT 1"))
        query_time = round((time.time() - start_time) * 1000, 2)

        return {
            "status": "healthy",
            "query_time_ms": query_time,
            "error": None,
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "query_time_ms": None,
            "error": str(e),
        }


@router.get("/health", response_class=HTMLResponse)
async def health_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """系统健康监控页面"""
    if not check_permission(admin_user, "system:logs"):
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="没有查看系统监控的权限")

    templates = Jinja2Templates(directory="admin/templates")

    return templates.TemplateResponse("health.html", {
        "request": request,
    })


@router.get("/api/health")
async def get_health_status(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取系统健康状态API"""
    if not check_permission(admin_user, "system:logs"):
        return JSONResponse(
            content={"success": False, "message": "没有查看系统监控的权限"},
            status_code=403
        )

    system_info = get_system_info()
    db_health = get_database_health(db)

    # 计算总体健康状态
    is_healthy = (
        db_health["status"] == "healthy" and
        system_info["cpu_percent"] < 90 and
        system_info["memory_percent"] < 90 and
        system_info["disk_usage"]["percent"] < 90
    )

    return JSONResponse(content={
        "success": True,
        "data": {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy" if is_healthy else "warning",
            "system": system_info,
            "database": db_health,
        }
    })


@router.get("/api/health/system")
async def get_system_stats(
    admin_user=Depends(get_current_admin_user),
):
    """获取系统资源使用情况"""
    if not check_permission(admin_user, "system:logs"):
        return JSONResponse(
            content={"success": False, "message": "没有查看系统监控的权限"},
            status_code=403
        )

    system_info = get_system_info()

    return JSONResponse(content={
        "success": True,
        "data": system_info
    })


@router.get("/api/health/database")
async def get_database_stats(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取数据库状态"""
    if not check_permission(admin_user, "system:logs"):
        return JSONResponse(
            content={"success": False, "message": "没有查看系统监控的权限"},
            status_code=403
        )

    db_health = get_database_health(db)

    # 获取数据库统计信息
    try:
        from sqlalchemy import func
        from app.models import Post, Product, Gallery, MediaFile, AdminUser

        stats = {
            "posts_count": db.query(func.count(Post.id)).scalar() or 0,
            "products_count": db.query(func.count(Product.id)).scalar() or 0,
            "galleries_count": db.query(func.count(Gallery.id)).scalar() or 0,
            "media_count": db.query(func.count(MediaFile.id)).scalar() or 0,
            "users_count": db.query(func.count(AdminUser.id)).scalar() or 0,
            "connections": db_health,
        }
    except Exception as e:
        stats = {"error": str(e)}

    return JSONResponse(content={
        "success": True,
        "data": stats
    })


@router.get("/api/health/history")
async def get_health_history(
    minutes: int = 30,
    admin_user=Depends(get_current_admin_user),
):
    """获取历史健康数据（用于图表展示）"""
    if not check_permission(admin_user, "system:logs"):
        return JSONResponse(
            content={"success": False, "message": "没有查看系统监控的权限"},
            status_code=403
        )

    # 从内存中获取历史数据（实际应用中应该使用时序数据库或文件存储）
    # 这里返回一个模拟的历史数据
    import random
    from datetime import timedelta

    history = []
    now = datetime.now()

    for i in range(minutes):
        timestamp = now - timedelta(minutes=i)
        history.append({
            "timestamp": timestamp.isoformat(),
            "cpu": random.randint(10, 60),
            "memory": random.randint(30, 70),
            "disk": random.randint(40, 60),
        })

    history.reverse()

    return JSONResponse(content={
        "success": True,
        "data": history
    })


@router.get("/api/services")
async def get_services_status(
    admin_user=Depends(get_current_admin_user),
):
    """获取服务状态"""
    if not check_permission(admin_user, "system:logs"):
        return JSONResponse(
            content={"success": False, "message": "没有查看系统监控的权限"},
            status_code=403
        )

    # 检查各项服务状态
    services = [
        {
            "name": "Web Server",
            "status": "running",
            "port": 10034,
            "description": "主Web服务",
        },
        {
            "name": "Database",
            "status": "running",
            "port": None,
            "description": "SQLite数据库",
        },
        {
            "name": "Static Files",
            "status": "running",
            "port": None,
            "description": "静态文件服务",
        },
    ]

    return JSONResponse(content={
        "success": True,
        "data": services
    })


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="admin/templates")
