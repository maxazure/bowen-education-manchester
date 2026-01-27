"""
静态页面管理路由
"""

import math
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from admin.app.database import get_db
from app.models.static_generation import StaticGenerationLog, StaticGenerationDetail
from app.services.static_generator import StaticPageGenerator

router = APIRouter(tags=["static-pages"])

templates = Jinja2Templates(directory="admin/templates")


def generate_static_task(output_dir: str = "public", base_url: str = "http://localhost:8000"):
    """
    后台任务：生成静态页面

    Args:
        output_dir: 输出目录
        base_url: 网站基础 URL
    """
    from app.database import SessionLocal
    import logging

    logger = logging.getLogger("docms")
    db = SessionLocal()

    try:
        logger.info(f"开始后台生成静态页面，输出目录: {output_dir}")
        generator = StaticPageGenerator(
            db=db,
            output_dir=output_dir,
            base_url=base_url,
        )
        log = generator.generate_all()
        logger.info(f"静态页面生成完成，总计: {log.total_pages} 页，成功: {log.successful_pages} 页，失败: {log.failed_pages} 页")
    except Exception as e:
        logger.error(f"后台生成静态页面失败: {str(e)}", exc_info=True)
    finally:
        db.close()


@router.get("", response_class=HTMLResponse)
async def list_static_generation_logs(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
):
    """
    静态页面生成历史列表

    Args:
        request: FastAPI request 对象
        db: 数据库会话
        page: 页码

    Returns:
        生成历史列表页面 HTML
    """
    # 分页查询
    page_size = 20
    query = db.query(StaticGenerationLog).order_by(desc(StaticGenerationLog.start_time))

    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    # 限制页码范围
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    offset = (page - 1) * page_size
    logs = query.limit(page_size).offset(offset).all()

    # 获取最新的一条记录
    latest_log = (
        db.query(StaticGenerationLog)
        .order_by(desc(StaticGenerationLog.start_time))
        .first()
    )

    # 检查 public 目录是否存在
    public_dir = Path("public")
    public_exists = public_dir.exists()

    # 统计 public 目录下的文件数量
    file_count = 0
    if public_exists:
        file_count = sum(1 for _ in public_dir.rglob("*.html"))

    return templates.TemplateResponse(
        "static_pages/index.html",
        {
            "request": request,
            "logs": logs,
            "latest_log": latest_log,
            "public_exists": public_exists,
            "file_count": file_count,
            "page": page,
            "total_pages": total_pages,
            "total": total,
        },
    )


@router.get("/{log_id}", response_class=HTMLResponse)
async def view_static_generation_log(
    request: Request,
    log_id: int,
    db: Session = Depends(get_db),
    page: int = 1,
):
    """
    查看生成日志详情

    Args:
        request: FastAPI request 对象
        log_id: 日志 ID
        db: 数据库会话
        page: 页码

    Returns:
        生成日志详情页面 HTML
    """
    # 获取日志记录
    log = db.query(StaticGenerationLog).filter(StaticGenerationLog.id == log_id).first()

    if not log:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "日志记录不存在"},
            status_code=404,
        )

    # 分页查询详情
    page_size = 50
    query = (
        db.query(StaticGenerationDetail)
        .filter(StaticGenerationDetail.log_id == log_id)
        .order_by(StaticGenerationDetail.id)
    )

    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    # 限制页码范围
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    offset = (page - 1) * page_size
    details = query.limit(page_size).offset(offset).all()

    # 按状态分组统计
    success_count = (
        db.query(StaticGenerationDetail)
        .filter(
            StaticGenerationDetail.log_id == log_id,
            StaticGenerationDetail.status == "success",
        )
        .count()
    )

    failed_count = (
        db.query(StaticGenerationDetail)
        .filter(
            StaticGenerationDetail.log_id == log_id,
            StaticGenerationDetail.status == "failed",
        )
        .count()
    )

    # 按页面类型统计
    type_stats = {}
    for detail in db.query(StaticGenerationDetail).filter(StaticGenerationDetail.log_id == log_id):
        if detail.page_type not in type_stats:
            type_stats[detail.page_type] = {"total": 0, "success": 0, "failed": 0}
        type_stats[detail.page_type]["total"] += 1
        if detail.status == "success":
            type_stats[detail.page_type]["success"] += 1
        else:
            type_stats[detail.page_type]["failed"] += 1

    return templates.TemplateResponse(
        "static_pages/detail.html",
        {
            "request": request,
            "log": log,
            "details": details,
            "success_count": success_count,
            "failed_count": failed_count,
            "type_stats": type_stats,
            "page": page,
            "total_pages": total_pages,
            "total": total,
        },
    )


@router.post("/generate", response_class=JSONResponse)
async def trigger_static_generation(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    触发静态页面生成

    Args:
        request: FastAPI request 对象
        background_tasks: 后台任务
        db: 数据库会话

    Returns:
        JSON 响应
    """
    try:
        # 检查是否有正在运行的生成任务
        running_log = (
            db.query(StaticGenerationLog)
            .filter(StaticGenerationLog.status == "running")
            .first()
        )

        if running_log:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": "已有生成任务正在运行，请稍后再试",
                },
            )

        # 添加后台任务
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "静态页面生成任务已启动，请稍后查看生成历史",
            },
        )

    except Exception as e:
        import logging
        logger = logging.getLogger("docms")
        logger.error(f"触发静态页面生成失败: {str(e)}", exc_info=True)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"触发生成失败: {str(e)}",
            },
        )


@router.delete("/{log_id}", response_class=JSONResponse)
async def delete_static_generation_log(
    log_id: int,
    db: Session = Depends(get_db),
):
    """
    删除生成日志

    Args:
        log_id: 日志 ID
        db: 数据库会话

    Returns:
        JSON 响应
    """
    try:
        log = db.query(StaticGenerationLog).filter(StaticGenerationLog.id == log_id).first()

        if not log:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "日志记录不存在",
                },
            )

        # 删除日志（详情会通过级联删除自动删除）
        db.delete(log)
        db.commit()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "日志记录已删除",
            },
        )

    except Exception as e:
        db.rollback()
        import logging
        logger = logging.getLogger("docms")
        logger.error(f"删除生成日志失败: {str(e)}", exc_info=True)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"删除失败: {str(e)}",
            },
        )


@router.get("/api/status/{log_id}", response_class=JSONResponse)
async def get_generation_status(
    log_id: int,
    db: Session = Depends(get_db),
):
    """
    获取生成任务状态（用于轮询）

    Args:
        log_id: 日志 ID
        db: 数据库会话

    Returns:
        JSON 响应包含任务状态
    """
    try:
        log = db.query(StaticGenerationLog).filter(StaticGenerationLog.id == log_id).first()

        if not log:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "message": "日志记录不存在",
                },
            )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": {
                    "id": log.id,
                    "status": log.status,
                    "total_pages": log.total_pages,
                    "successful_pages": log.successful_pages,
                    "failed_pages": log.failed_pages,
                    "start_time": log.start_time.isoformat() if log.start_time else None,
                    "end_time": log.end_time.isoformat() if log.end_time else None,
                },
            },
        )

    except Exception as e:
        import logging
        logger = logging.getLogger("docms")
        logger.error(f"获取生成状态失败: {str(e)}", exc_info=True)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"获取状态失败: {str(e)}",
            },
        )
