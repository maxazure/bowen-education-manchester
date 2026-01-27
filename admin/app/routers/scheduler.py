"""
定时任务管理路由

管理后台定时任务配置和监控
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from enum import Enum

from fastapi import APIRouter, Depends, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy import func, Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user, require_super_admin
from app.models import AdminUser

router = APIRouter(tags=["scheduler"])


# 任务状态枚举
class TaskStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


# 任务类型枚举
class TaskType(str, Enum):
    SITEMAP = "sitemap"
    BACKUP = "backup"
    CLEANUP = "cleanup"
    SYNC = "sync"
    NOTIFICATION = "notification"
    CUSTOM = "custom"


# Pydantic models for API
class TaskCreate(BaseModel):
    name: str
    task_type: TaskType
    cron_expression: str
    description: Optional[str] = None
    config: Optional[Dict] = None
    enabled: bool = True


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    cron_expression: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict] = None
    enabled: Optional[bool] = None


class TaskExecute(BaseModel):
    task_id: int


# 模拟任务存储（实际项目中可以使用数据库或Redis）
_task_store: Dict[int, Dict] = {}
_task_counter = 0


def _generate_id():
    global _task_counter
    _task_counter += 1
    return _task_counter


# 预定义任务模板
TASK_TEMPLATES = {
    "sitemap": {
        "name": "生成网站地图",
        "task_type": "sitemap",
        "cron_expression": "0 2 * * *",
        "description": "每天凌晨2点自动生成 sitemap.xml",
        "icon": "bi-globe",
        "color": "#667eea"
    },
    "backup": {
        "name": "数据库备份",
        "task_type": "backup",
        "cron_expression": "0 3 * * 0",
        "description": "每周日凌晨3点备份数据库",
        "icon": "bi-hdd",
        "color": "#43e97b"
    },
    "cleanup_logs": {
        "name": "清理日志文件",
        "task_type": "cleanup",
        "cron_expression": "0 4 1 * *",
        "description": "每月凌晨4点清理30天前的日志",
        "icon": "bi-trash",
        "color": "#fa709a"
    },
    "cleanup_versions": {
        "name": "清理旧版本",
        "task_type": "cleanup",
        "cron_expression": "0 5 1 * *",
        "description": "每月凌晨5点清理90天前的版本历史",
        "icon": "bi-clock-history",
        "color": "#fee140"
    },
    "sync_data": {
        "name": "数据同步",
        "task_type": "sync",
        "cron_expression": "0 */6 * * *",
        "description": "每6小时同步一次外部数据",
        "icon": "bi-arrow-repeat",
        "color": "#4facfe"
    },
    "health_check": {
        "name": "健康检查通知",
        "task_type": "notification",
        "cron_expression": "0 8 * * *",
        "description": "每天早上8点发送系统健康报告",
        "icon": "bi-heart-pulse",
        "color": "#ff6b6b"
    }
}


def _parse_cron(cron: str) -> Dict[str, str]:
    """解析cron表达式"""
    parts = cron.split()
    if len(parts) != 5:
        return {"error": "Invalid cron expression"}
    return {
        "minute": parts[0],
        "hour": parts[1],
        "day": parts[2],
        "month": parts[3],
        "weekday": parts[4]
    }


def _format_next_run(cron: str) -> str:
    """计算下次执行时间"""
    # 简化实现，返回下次执行时间估算
    parts = cron.split()
    if len(parts) != 5:
        return "未知"

    minute, hour, day, month, weekday = parts

    now = datetime.now()

    # 处理通配符
    if hour == "*":
        next_hour = now.hour
    elif hour.startswith("*/"):
        # 每隔几小时执行
        interval = int(hour[2:])
        next_hour = now.hour + interval
        if next_hour >= 24:
            next_hour = now.hour
            next_time = now.replace(hour=now.hour, minute=0, second=0, microsecond=0) + timedelta(days=1)
            return next_time.strftime("%Y-%m-%d %H:%M")
    else:
        try:
            next_hour = int(hour)
            if next_hour < now.hour:
                return "明天"
        except ValueError:
            return "明天"

    if minute == "*":
        next_minute = 0
    elif minute.startswith("*/"):
        interval = int(minute[2:])
        next_minute = (now.minute // interval + 1) * interval
        if next_minute >= 60:
            next_minute = 0
            next_hour += 1
            if next_hour >= 24:
                next_hour = 0
                next_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                return next_time.strftime("%Y-%m-%d %H:%M")
    else:
        try:
            next_minute = int(minute)
        except ValueError:
            next_minute = 0

    next_time = now.replace(hour=next_hour, minute=next_minute, second=0, microsecond=0)

    if next_time <= now:
        next_time += timedelta(days=1)

    return next_time.strftime("%Y-%m-%d %H:%M")


@router.get("/scheduler", response_class=HTMLResponse)
async def scheduler_page(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """定时任务管理页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 获取所有任务
    tasks = list(_task_store.values())

    # 计算统计数据
    stats = {
        "total": len(tasks),
        "active": len([t for t in tasks if t["status"] == "active"]),
        "paused": len([t for t in tasks if t["status"] == "paused"]),
        "failed": len([t for t in tasks if t["status"] == "failed"]),
        "total_runs": sum(t.get("run_count", 0) for t in tasks)
    }

    return templates.TemplateResponse("scheduler.html", {
        "request": request,
        "tasks": tasks,
        "templates": TASK_TEMPLATES,
        "stats": stats,
        "cron_parts": _parse_cron("0 2 * * *")
    })


@router.get("/api/scheduler/list")
async def get_scheduler_list(
    status: Optional[str] = None,
    task_type: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取任务列表"""
    tasks = list(_task_store.values())

    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if task_type:
        tasks = [t for t in tasks if t["task_type"] == task_type]

    return JSONResponse(content={
        "success": True,
        "data": tasks
    })


@router.get("/api/scheduler/templates")
async def get_task_templates(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取任务模板"""
    return JSONResponse(content={
        "success": True,
        "data": TASK_TEMPLATES
    })


@router.post("/api/scheduler/create")
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    admin_user=Depends(require_super_admin),
):
    """创建新任务"""
    task_id = _generate_id()

    new_task = {
        "id": task_id,
        "name": task.name,
        "task_type": task.task_type.value if isinstance(task.task_type, Enum) else task.task_type,
        "cron_expression": task.cron_expression,
        "description": task.description or "",
        "config": task.config or {},
        "enabled": task.enabled,
        "status": "active" if task.enabled else "paused",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "last_run": None,
        "last_result": None,
        "run_count": 0,
        "next_run": _format_next_run(task.cron_expression)
    }

    _task_store[task_id] = new_task

    return JSONResponse(content={
        "success": True,
        "message": "任务创建成功",
        "data": new_task
    })


@router.post("/api/scheduler/from-template")
async def create_from_template(
    template_key: str = Query(...),
    db: Session = Depends(get_db),
    admin_user=Depends(require_super_admin),
):
    """从模板创建任务"""
    if template_key not in TASK_TEMPLATES:
        return JSONResponse(
            content={"success": False, "message": "模板不存在"},
            status_code=404
        )

    template = TASK_TEMPLATES[template_key]
    task_id = _generate_id()

    new_task = {
        "id": task_id,
        "name": template["name"],
        "task_type": template["task_type"],
        "cron_expression": template["cron_expression"],
        "description": template["description"],
        "config": {},
        "enabled": True,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "last_run": None,
        "last_result": None,
        "run_count": 0,
        "next_run": _format_next_run(template["cron_expression"]),
        "icon": template.get("icon", "bi-gear"),
        "color": template.get("color", "#667eea")
    }

    _task_store[task_id] = new_task

    return JSONResponse(content={
        "success": True,
        "message": "任务创建成功",
        "data": new_task
    })


@router.get("/api/scheduler/{task_id}")
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取任务详情"""
    task = _task_store.get(task_id)
    if not task:
        return JSONResponse(
            content={"success": False, "message": "任务不存在"},
            status_code=404
        )

    return JSONResponse(content={
        "success": True,
        "data": task
    })


@router.put("/api/scheduler/{task_id}")
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    admin_user=Depends(require_super_admin),
):
    """更新任务"""
    if task_id not in _task_store:
        return JSONResponse(
            content={"success": False, "message": "任务不存在"},
            status_code=404
        )

    existing_task = _task_store[task_id]

    if task.name is not None:
        existing_task["name"] = task.name
    if task.cron_expression is not None:
        existing_task["cron_expression"] = task.cron_expression
        existing_task["next_run"] = _format_next_run(task.cron_expression)
    if task.description is not None:
        existing_task["description"] = task.description
    if task.config is not None:
        existing_task["config"] = task.config
    if task.enabled is not None:
        existing_task["enabled"] = task.enabled
        existing_task["status"] = "active" if task.enabled else "paused"

    existing_task["updated_at"] = datetime.now().isoformat()

    return JSONResponse(content={
        "success": True,
        "message": "任务更新成功",
        "data": existing_task
    })


@router.delete("/api/scheduler/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(require_super_admin),
):
    """删除任务"""
    if task_id not in _task_store:
        return JSONResponse(
            content={"success": False, "message": "任务不存在"},
            status_code=404
        )

    del _task_store[task_id]

    return JSONResponse(content={
        "success": True,
        "message": "任务删除成功"
    })


@router.post("/api/scheduler/{task_id}/toggle")
async def toggle_task(
    task_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(require_super_admin),
):
    """切换任务状态"""
    if task_id not in _task_store:
        return JSONResponse(
            content={"success": False, "message": "任务不存在"},
            status_code=404
        )

    task = _task_store[task_id]
    task["enabled"] = not task["enabled"]
    task["status"] = "active" if task["enabled"] else "paused"
    task["updated_at"] = datetime.now().isoformat()

    return JSONResponse(content={
        "success": True,
        "message": f"任务已{'启用' if task['enabled'] else '暂停'}",
        "data": task
    })


@router.post("/api/scheduler/{task_id}/execute")
async def execute_task(
    task_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(require_super_admin),
):
    """立即执行任务"""
    if task_id not in _task_store:
        return JSONResponse(
            content={"success": False, "message": "任务不存在"},
            status_code=404
        )

    task = _task_store[task_id]

    # 模拟任务执行
    import random

    # 模拟执行延迟
    import time
    time.sleep(0.5)

    # 模拟执行结果
    success = random.random() > 0.1  # 90% 成功率

    task["last_run"] = datetime.now().isoformat()
    task["last_result"] = "success" if success else "failed"
    task["run_count"] += 1
    task["next_run"] = _format_next_run(task["cron_expression"])

    return JSONResponse(content={
        "success": True,
        "message": "任务执行完成" if success else "任务执行失败",
        "data": {
            "success": success,
            "executed_at": task["last_run"],
            "result": task["last_result"]
        }
    })


@router.get("/api/scheduler/{task_id}/logs")
async def get_task_logs(
    task_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取任务执行日志"""
    if task_id not in _task_store:
        return JSONResponse(
            content={"success": False, "message": "任务不存在"},
            status_code=404
        )

    # 生成模拟日志
    logs = []
    for i in range(min(limit, 50)):
        timestamp = datetime.now() - timedelta(hours=i * 6 + random.randint(0, 5))
        success = random.random() > 0.1

        logs.append({
            "id": i + 1,
            "timestamp": timestamp.isoformat(),
            "status": "success" if success else "failed",
            "duration": random.randint(1, 300),
            "message": f"任务执行{'成功' if success else '失败'}，耗时 {random.randint(1, 300)} 秒"
        })

    return JSONResponse(content={
        "success": True,
        "data": logs
    })


@router.get("/api/scheduler/stats/overview")
async def get_scheduler_stats(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取调度器统计信息"""
    tasks = list(_task_store.values())

    stats = {
        "total": len(tasks),
        "active": len([t for t in tasks if t["status"] == "active"]),
        "paused": len([t for t in tasks if t["status"] == "paused"]),
        "failed": len([t for t in tasks if t["status"] == "failed"]),
        "total_runs": sum(t.get("run_count", 0) for t in tasks),
        "success_rate": 0,
    }

    # 计算成功率
    total_runs = stats["total_runs"]
    if total_runs > 0:
        success_count = sum(1 for t in tasks if t.get("last_result") == "success")
        stats["success_rate"] = round(success_count / len(tasks) * 100, 1) if tasks else 0

    # 按类型统计
    type_stats = {}
    for task in tasks:
        task_type = task["task_type"]
        if task_type not in type_stats:
            type_stats[task_type] = {"count": 0, "active": 0}
        type_stats[task_type]["count"] += 1
        if task["status"] == "active":
            type_stats[task_type]["active"] += 1

    stats["by_type"] = type_stats

    return JSONResponse(content={
        "success": True,
        "data": stats
    })


# 初始化默认任务
def _init_default_tasks():
    """初始化默认任务"""
    global _task_store

    if len(_task_store) > 0:
        return  # 已初始化

    for key, template in TASK_TEMPLATES.items():
        task_id = _generate_id()
        task = {
            "id": task_id,
            "name": template["name"],
            "task_type": template["task_type"],
            "cron_expression": template["cron_expression"],
            "description": template["description"],
            "config": {},
            "enabled": True,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "last_run": None,
            "last_result": None,
            "run_count": 0,
            "next_run": _format_next_run(template["cron_expression"]),
            "icon": template.get("icon", "bi-gear"),
            "color": template.get("color", "#667eea"),
            "is_template": True
        }
        _task_store[task_id] = task


# 初始化默认任务
_init_default_tasks()
