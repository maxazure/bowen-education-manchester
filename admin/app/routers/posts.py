"""
文章管理路由
"""

import json
import math
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models.post import Post, PostCategory
from app.models.site import ColumnType, SiteColumn
from app.services.post_service import (can_delete_post, generate_slug,
                                       publish_post, unpublish_post)
from app.services.single_page_service import markdown_to_html
from admin.app.routers.static_pages import generate_static_task

router = APIRouter(tags=["posts"])

templates = Jinja2Templates(directory="admin/templates")


def parse_optional_int(value: Optional[str]) -> Optional[int]:
    """Convert empty string to None for optional integer fields"""
    if value == "" or value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


@router.get("", response_class=HTMLResponse)
async def list_posts(
    request: Request,
    db: Session = Depends(get_db),
    column_id: Optional[int] = None,
    category: Optional[str] = None,
    status_filter: Optional[str] = None,
    keyword: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
):
    """
    文章列表页

    支持筛选: column_id, category, status, keyword, start_date, end_date, page
    """
    from datetime import datetime

    # 基础查询
    query = db.query(Post).options(
        joinedload(Post.column),
        joinedload(Post.categories),
    )

    # 筛选条件
    if column_id:
        query = query.filter(Post.column_id == column_id)

    if category:
        query = query.join(Post.categories).filter(PostCategory.slug == category)

    if status_filter:
        query = query.filter(Post.status == status_filter)

    if keyword:
        query = query.filter(
            (Post.title.contains(keyword)) | (Post.summary.contains(keyword))
        )

    # 日期范围筛选
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Post.created_at >= start)
        except ValueError:
            pass

    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            # 设置为当天的最后时刻
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(Post.created_at <= end)
        except ValueError:
            pass

    # 排序: 置顶文章优先,然后按更新时间
    query = query.order_by(Post.is_pinned.desc(), Post.updated_at.desc())

    # 分页 - 验证 page_size 范围
    page_size = max(1, min(100, page_size))
    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    # 限制页码范围
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    offset = (page - 1) * page_size
    posts = query.limit(page_size).offset(offset).all()

    # 获取所有栏目（类型为 POST）
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.column_type == ColumnType.POST)
        .order_by(SiteColumn.sort_order)
        .all()
    )

    # 获取所有分类
    categories = db.query(PostCategory).order_by(PostCategory.sort_order).all()

    # 统计数据（用于快速筛选）
    total_posts = db.query(Post).count()
    published_count = db.query(Post).filter(Post.status == "published").count()
    draft_count = db.query(Post).filter(Post.status == "draft").count()
    offline_count = db.query(Post).filter(Post.status == "offline").count()
    recommended_count = db.query(Post).filter(Post.is_recommended == True).count()
    pinned_count = db.query(Post).filter(Post.is_pinned == True).count()

    # 构建页面URL的辅助函数
    def build_page_url(p):
        params = []
        if column_id:
            params.append(f"column_id={column_id}")
        if status_filter:
            params.append(f"status_filter={status_filter}")
        if keyword:
            params.append(f"keyword={keyword}")
        params.append(f"page={p}")
        return f"/admin/posts?{'&'.join(params)}"

    return templates.TemplateResponse(
        "posts/list.html",
        {
            "request": request,
            "posts": posts,
            "columns": columns,
            "categories": categories,
            "current_column_id": column_id,
            "current_category": category,
            "current_status": status_filter,
            "current_keyword": keyword,
            "start_date": start_date,
            "end_date": end_date,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "total": total,
            "total_posts": total_posts,
            "published_count": published_count,
            "draft_count": draft_count,
            "offline_count": offline_count,
            "recommended_count": recommended_count,
            "pinned_count": pinned_count,
            "build_page_url": build_page_url,
        },
    )


@router.get("/new", response_class=HTMLResponse)
async def new_post_form(
    request: Request,
    db: Session = Depends(get_db),
):
    """新建文章表单"""
    # 获取所有栏目（类型为 POST）
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.column_type == ColumnType.POST)
        .order_by(SiteColumn.sort_order)
        .all()
    )

    # 获取所有分类
    categories = db.query(PostCategory).order_by(PostCategory.sort_order).all()

    return templates.TemplateResponse(
        "posts/form.html",
        {
            "request": request,
            "post": None,
            "columns": columns,
            "categories": categories,
            "action": "/admin/posts/create",
            "method": "POST",
        },
    )


@router.post("/create", response_class=JSONResponse)
async def create_post(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    column_id: int = Form(...),
    title: str = Form(...),
    slug: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    content_markdown: Optional[str] = Form(None),
    cover_media_id: Optional[str] = Form(None),  # 接收字符串，转换为整数
    category_ids: str = Form(""),  # 逗号分隔的分类 ID
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    # 英文字段
    title_en: Optional[str] = Form(None),
    summary_en: Optional[str] = Form(None),
    content_markdown_en: Optional[str] = Form(None),
    seo_title_en: Optional[str] = Form(None),
    seo_description_en: Optional[str] = Form(None),
    # 其他字段
    is_recommended: bool = Form(False),
    is_pinned: bool = Form(False),
    status_val: str = Form("draft"),
):
    """创建文章"""
    try:
        # 导入 slug 生成函数
        from app.services.post_service import generate_slug as post_generate_slug

        # 生成或验证 slug
        if not slug:
            slug = post_generate_slug(title, db)
        else:
            # 验证 slug 是否已存在
            existing_slug = slug
            counter = 1
            while True:
                existing = db.query(Post).filter(Post.slug == existing_slug).first()
                if not existing:
                    slug = existing_slug
                    break
                existing_slug = f"{slug}-{counter}"
                counter += 1

        # 解析 cover_media_id（字符串转整数）
        parsed_cover_media_id = parse_optional_int(cover_media_id)

        # 转换中文 Markdown 为 HTML
        content_html = ""
        if content_markdown:
            content_html = markdown_to_html(content_markdown)

        # 转换英文 Markdown 为 HTML
        content_html_en = ""
        if content_markdown_en:
            content_html_en = markdown_to_html(content_markdown_en)

        # 创建文章
        post = Post(
            column_id=column_id,
            title=title,
            slug=slug,
            summary=summary,
            content_markdown=content_markdown,
            content_html=content_html,
            cover_media_id=parsed_cover_media_id,
            seo_title=seo_title,
            seo_description=seo_description,
            # 英文字段
            title_en=title_en,
            summary_en=summary_en,
            content_markdown_en=content_markdown_en,
            content_html_en=content_html_en,
            seo_title_en=seo_title_en,
            seo_description_en=seo_description_en,
            # 其他字段
            is_recommended=is_recommended,
            is_pinned=is_pinned,
            status=status_val,
        )

        db.add(post)
        db.flush()  # 获取 post.id

        # 设置分类
        if category_ids:
            cat_ids = [
                int(cid.strip()) for cid in category_ids.split(",") if cid.strip()
            ]
            categories = (
                db.query(PostCategory).filter(PostCategory.id.in_(cat_ids)).all()
            )
            post.categories = categories

        db.commit()
        db.refresh(post)

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={"success": True, "message": "文章创建成功", "post_id": post.id},
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"创建失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/{post_id}", response_class=JSONResponse)
async def get_post_json(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db),
):
    """获取文章JSON数据（用于快速预览等）"""
    post = (
        db.query(Post)
        .options(joinedload(Post.column))
        .filter(Post.id == post_id)
        .first()
    )

    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=404
        )

    return JSONResponse(content={
        "success": True,
        "post": {
            "id": post.id,
            "title": post.title,
            "title_en": post.title_en,
            "summary": post.summary,
            "summary_en": post.summary_en,
            "content_html": post.content_html,
            "content_html_en": post.content_html_en,
            "content_markdown": post.content_markdown,
            "content_markdown_en": post.content_markdown_en,
            "seo_title": post.seo_title,
            "seo_title_en": post.seo_title_en,
            "seo_description": post.seo_description,
            "seo_description_en": post.seo_description_en,
            "status": post.status,
            "column_id": post.column_id,
            "column_name": post.column.name if post.column else None,
            "view_count": post.view_count,
            "is_recommended": post.is_recommended,
            "is_pinned": post.is_pinned,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S") if post.created_at else None,
            "updated_at": post.updated_at.strftime("%Y-%m-%d %H:%M:%S") if post.updated_at else None,
            "published_at": post.published_at.strftime("%Y-%m-%d %H:%M:%S") if post.published_at else None,
        }
    })


@router.get("/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_form(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db),
):
    """编辑文章表单"""
    post = (
        db.query(Post)
        .options(joinedload(Post.categories))
        .filter(Post.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 获取所有栏目（类型为 POST）
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.column_type == ColumnType.POST)
        .order_by(SiteColumn.sort_order)
        .all()
    )

    # 获取所有分类
    categories = db.query(PostCategory).order_by(PostCategory.sort_order).all()

    return templates.TemplateResponse(
        "posts/form.html",
        {
            "request": request,
            "post": post,
            "columns": columns,
            "categories": categories,
            "action": f"/admin/posts/{post_id}",
            "method": "POST",
        },
    )


@router.post("/{post_id}", response_class=JSONResponse)
async def update_post(
    request: Request,
    post_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    column_id: int = Form(...),
    title: str = Form(...),
    slug: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    content_markdown: Optional[str] = Form(None),
    cover_media_id: Optional[str] = Form(None),  # 接收字符串，转换为整数
    category_ids: str = Form(""),
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    # 英文字段
    title_en: Optional[str] = Form(None),
    summary_en: Optional[str] = Form(None),
    content_markdown_en: Optional[str] = Form(None),
    seo_title_en: Optional[str] = Form(None),
    seo_description_en: Optional[str] = Form(None),
    # 其他字段
    is_recommended: bool = Form(False),
    is_pinned: bool = Form(False),
    status_val: str = Form("draft"),
):
    """更新文章"""
    try:
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(status_code=404, detail="文章不存在")

        # 更新 slug (验证或生成唯一 slug)
        if not slug:
            slug = generate_slug(title, db, exclude_id=post_id)
        else:
            # 验证 slug 是否已存在（排除当前文章）
            existing_slug = slug
            counter = 1
            while True:
                existing = db.query(Post).filter(
                    Post.slug == existing_slug,
                    Post.id != post_id
                ).first()
                if not existing:
                    slug = existing_slug
                    break
                existing_slug = f"{slug}-{counter}"
                counter += 1

        # 解析 cover_media_id（字符串转整数）
        parsed_cover_media_id = parse_optional_int(cover_media_id)

        # 转换中文 Markdown 为 HTML
        content_html = post.content_html
        if content_markdown:
            content_html = markdown_to_html(content_markdown)

        # 转换英文 Markdown 为 HTML
        content_html_en = post.content_html_en if hasattr(post, 'content_html_en') else ""
        if content_markdown_en:
            content_html_en = markdown_to_html(content_markdown_en)

        # 更新中文字段
        post.column_id = column_id
        post.title = title
        post.slug = slug
        post.summary = summary
        post.content_markdown = content_markdown
        post.content_html = content_html
        post.cover_media_id = parsed_cover_media_id
        post.seo_title = seo_title
        post.seo_description = seo_description

        # 更新英文字段
        post.title_en = title_en
        post.summary_en = summary_en
        post.content_markdown_en = content_markdown_en
        post.content_html_en = content_html_en
        post.seo_title_en = seo_title_en
        post.seo_description_en = seo_description_en

        # 更新其他字段
        post.is_recommended = is_recommended
        post.is_pinned = is_pinned
        post.status = status_val

        # 更新分类
        if category_ids:
            cat_ids = [
                int(cid.strip()) for cid in category_ids.split(",") if cid.strip()
            ]
            categories = (
                db.query(PostCategory).filter(PostCategory.id.in_(cat_ids)).all()
            )
            post.categories = categories
        else:
            post.categories = []

        db.commit()

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={"success": True, "message": "文章更新成功"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"更新失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.delete("/{post_id}", response_class=JSONResponse)
async def delete_post(
    post_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """删除文章（移到回收站）"""
    # 检查是否可以删除
    can_delete, error_msg = can_delete_post(db, post_id)

    if not can_delete:
        return JSONResponse(
            content={"success": False, "message": error_msg},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(status_code=404, detail="文章不存在")

        # 软删除：移到回收站
        post.status = "trashed"
        db.commit()

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={"success": True, "message": "文章已移到回收站，可在回收站恢复"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/{post_id}/publish", response_class=JSONResponse)
async def toggle_publish_post(
    post_id: int,
    db: Session = Depends(get_db),
    action: str = Form(...),  # "publish" or "unpublish"
):
    """发布/取消发布文章"""
    try:
        if action == "publish":
            success, message = publish_post(db, post_id)
        elif action == "unpublish":
            success, message = unpublish_post(db, post_id)
        else:
            return JSONResponse(
                content={"success": False, "message": "无效的操作"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if success:
            return JSONResponse(
                content={"success": True, "message": message},
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                content={"success": False, "message": message},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"操作失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/{post_id}/schedule", response_class=JSONResponse)
async def schedule_post(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    """设置文章定时发布"""
    from datetime import datetime

    try:
        data = await request.json()
        scheduled_time = data.get("scheduled_at")

        if not scheduled_time:
            return JSONResponse(
                content={"success": False, "message": "请选择定时发布时间"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 解析时间
        try:
            scheduled_dt = datetime.fromisoformat(scheduled_time.replace("Z", "+00:00"))
        except ValueError:
            return JSONResponse(
                content={"success": False, "message": "时间格式无效，请使用 ISO 格式"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 检查时间是否在未来
        if scheduled_dt <= datetime.now():
            return JSONResponse(
                content={"success": False, "message": "定时发布时间必须在未来"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return JSONResponse(
                content={"success": False, "message": "文章不存在"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        post.scheduled_at = scheduled_dt
        post.status = "draft"  # 定时发布的文章保持草稿状态
        post.updated_at = func.now()
        db.commit()

        return JSONResponse(
            content={
                "success": True,
                "message": f"已设置定时发布: {scheduled_dt.strftime('%Y-%m-%d %H:%M')}"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"设置失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/{post_id}/cancel-schedule", response_class=JSONResponse)
async def cancel_schedule(
    post_id: int,
    db: Session = Depends(get_db),
):
    """取消定时发布"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    post.scheduled_at = None
    post.updated_at = func.now()
    db.commit()

    return JSONResponse(
        content={"success": True, "message": "已取消定时发布"},
        status_code=status.HTTP_200_OK,
    )


@router.get("/scheduled", response_class=HTMLResponse)
async def scheduled_posts_list(
    request: Request,
    db: Session = Depends(get_db),
):
    """定时发布文章列表"""
    from datetime import datetime

    # 获取已设置定时发布的文章
    scheduled_posts = db.query(Post).filter(
        Post.scheduled_at.isnot(None),
        Post.scheduled_at > datetime.now()
    ).order_by(Post.scheduled_at).all()

    # 获取已过时的定时发布（应发布但未发布的）
    overdue_posts = db.query(Post).filter(
        Post.scheduled_at.isnot(None),
        Post.scheduled_at <= datetime.now(),
        Post.status == "draft"
    ).all()

    return templates.TemplateResponse("posts/scheduled.html", {
        "request": request,
        "posts": scheduled_posts,
        "overdue_posts": overdue_posts,
    })


@router.post("/batch/pin", response_class=JSONResponse)
async def batch_pin_posts(
    request: Request,
    db: Session = Depends(get_db),
):
    """批量置顶/取消置顶文章"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])
        is_pinned = data.get("is_pinned", True)

        if not post_ids or not isinstance(post_ids, list):
            return JSONResponse(
                content={"success": False, "message": "无效的文章ID列表"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 更新所有文章
        db.query(Post).filter(Post.id.in_(post_ids)).update(
            {Post.is_pinned: is_pinned, Post.updated_at: func.now()},
            synchronize_session=False
        )
        db.commit()

        action_text = "置顶" if is_pinned else "取消置顶"
        return JSONResponse(
            content={
                "success": True,
                "message": f"成功{action_text} {len(post_ids)} 篇文章"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"操作失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/offline", response_class=JSONResponse)
async def batch_offline_posts(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """批量下线文章"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])

        if not post_ids or not isinstance(post_ids, list):
            return JSONResponse(
                content={"success": False, "message": "无效的文章ID列表"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 更新所有文章状态为下线
        db.query(Post).filter(Post.id.in_(post_ids)).update(
            {Post.status: "offline", Post.updated_at: func.now()},
            synchronize_session=False
        )
        db.commit()

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"成功下线 {len(post_ids)} 篇文章"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"操作失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/column", response_class=JSONResponse)
async def batch_change_column(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """批量修改文章栏目"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])
        column_id = data.get("column_id")

        if not post_ids or not isinstance(post_ids, list):
            return JSONResponse(
                content={"success": False, "message": "无效的文章ID列表"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not column_id:
            return JSONResponse(
                content={"success": False, "message": "请选择目标栏目"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 验证栏目是否存在
        column = db.query(SiteColumn).filter(SiteColumn.id == column_id).first()
        if not column:
            return JSONResponse(
                content={"success": False, "message": "目标栏目不存在"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 更新所有文章的栏目
        db.query(Post).filter(Post.id.in_(post_ids)).update(
            {Post.column_id: column_id, Post.updated_at: func.now()},
            synchronize_session=False
        )
        db.commit()

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"成功将 {len(post_ids)} 篇文章移动到栏目「{column.name}」"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"操作失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/cover", response_class=JSONResponse)
async def batch_set_cover(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """批量设置文章封面"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])
        cover_image = data.get("cover_image", "")

        if not post_ids:
            return JSONResponse(
                content={"success": False, "message": "请选择文章"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not cover_image:
            return JSONResponse(
                content={"success": False, "message": "请选择封面图片"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 更新所有选中文章的封面
        db.query(Post).filter(Post.id.in_(post_ids)).update(
            {Post.cover_image: cover_image, Post.updated_at: func.now()},
            synchronize_session=False
        )
        db.commit()

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"成功为 {len(post_ids)} 篇文章设置封面"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"操作失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/check-slug", response_class=JSONResponse)
async def check_slug_unique(
    slug: str,
    exclude_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """检查 slug 是否唯一"""
    try:
        query = db.query(Post).filter(Post.slug == slug)
        if exclude_id:
            query = query.filter(Post.id != exclude_id)

        existing = query.first()

        return JSONResponse(
            content={
                "success": True,
                "available": existing is None,
                "message": "Slug 可用" if existing is None else "Slug 已被使用"
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"检查失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/duplicate/{post_id}", response_class=JSONResponse)
async def duplicate_post(
    post_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """复制文章"""
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return JSONResponse(
                content={"success": False, "message": "文章不存在"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # 生成新的 slug
        from app.services.post_service import generate_slug as post_generate_slug
        new_slug = post_generate_slug(post.title + "-copy", db)

        # 创建新文章（复制所有字段）
        new_post = Post(
            column_id=post.column_id,
            title=post.title + " (副本)",
            slug=new_slug,
            summary=post.summary,
            content_markdown=post.content_markdown,
            content_html=post.content_html,
            cover_media_id=post.cover_media_id,
            seo_title=post.seo_title,
            seo_description=post.seo_description,
            title_en=post.title_en,
            summary_en=post.summary_en,
            content_markdown_en=post.content_markdown_en,
            content_html_en=post.content_html_en,
            seo_title_en=post.seo_title_en,
            seo_description_en=post.seo_description_en,
            is_recommended=False,  # 副本不继承推荐
            is_pinned=False,  # 副本不继承置顶
            status="draft",  # 副本默认为草稿
        )

        db.add(new_post)
        db.flush()

        # 复制分类
        new_post.categories = post.categories

        db.commit()
        db.refresh(new_post)

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"文章复制成功，新文章 ID: {new_post.id}",
                "new_post_id": new_post.id
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"复制失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/export")
async def export_posts(
    request: Request,
    db: Session = Depends(get_db),
    column_id: Optional[int] = None,
    category: Optional[str] = None,
    status_filter: Optional[str] = None,
    keyword: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    format: str = Query(default="csv", regex="^(csv|xlsx)$"),
):
    """
    导出文章数据
    """
    from datetime import datetime
    import csv
    from io import StringIO
    from fastapi.responses import StreamingResponse

    # 基础查询
    query = db.query(Post).options(
        joinedload(Post.column),
        joinedload(Post.categories),
    )

    # 筛选条件
    if column_id:
        query = query.filter(Post.column_id == column_id)

    if category:
        query = query.join(Post.categories).filter(PostCategory.slug == category)

    if status_filter:
        query = query.filter(Post.status == status_filter)

    if keyword:
        query = query.filter(
            (Post.title.contains(keyword)) | (Post.summary.contains(keyword))
        )

    # 日期范围筛选
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Post.created_at >= start)
        except ValueError:
            pass

    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(Post.created_at <= end)
        except ValueError:
            pass

    # 排序
    query = query.order_by(Post.is_pinned.desc(), Post.created_at.desc())

    posts = query.all()

    # 生成 CSV
    output = StringIO()
    writer = csv.writer(output)

    # 写入表头
    writer.writerow([
        'ID', '标题', 'URL Slug', '摘要', '栏目', '分类',
        '状态', '推荐', '置顶', '创建时间', '更新时间',
        'SEO标题', 'SEO描述', '英文标题', '英文摘要'
    ])

    # 写入数据
    for post in posts:
        writer.writerow([
            post.id,
            post.title,
            post.slug or '',
            (post.summary or '')[:200],
            post.column.name if post.column else '',
            ', '.join([c.name for c in post.categories]),
            {'draft': '草稿', 'published': '已发布', 'offline': '已下线'}.get(post.status, post.status),
            '是' if post.is_recommended else '否',
            '是' if post.is_pinned else '否',
            post.created_at.strftime('%Y-%m-%d %H:%M:%S') if post.created_at else '',
            post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else '',
            post.seo_title or '',
            (post.seo_description or '')[:200],
            post.title_en or '',
            (post.summary_en or '')[:200],
        ])

    # 返回 CSV 文件
    filename = f"posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    response = StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response


@router.post("/import", response_class=JSONResponse)
async def import_posts(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    导入文章（支持 CSV、JSON、Markdown 格式）
    """
    from datetime import datetime
    from markdown import markdown as md_to_html

    try:
        data = await request.json()
        articles = data.get("data", [])
        column_id = data.get("column_id")
        status = data.get("status", "draft")
        import_type = data.get("type", "csv")

        if not articles:
            return JSONResponse(
                content={"success": False, "message": "没有可导入的文章数据"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not column_id:
            return JSONResponse(
                content={"success": False, "message": "请选择目标栏目"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 验证栏目
        column = db.query(SiteColumn).filter(SiteColumn.id == column_id).first()
        if not column:
            return JSONResponse(
                content={"success": False, "message": "目标栏目不存在"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        imported = 0
        skipped = 0
        errors = []

        # 导入slug生成函数
        from app.services.post_service import generate_slug

        for i, article in enumerate(articles):
            try:
                title = article.get("title", "").strip()
                if not title:
                    skipped += 1
                    continue

                summary = article.get("summary", "").strip() or ""
                content = article.get("content", "").strip() or ""

                # 转换 Markdown 到 HTML
                content_html = md_to_html(content) if content else ""

                # 处理状态
                article_status = article.get("status", status)
                if article_status not in ["draft", "published", "offline"]:
                    article_status = "draft"

                # 是否推荐
                is_recommended = article.get("is_recommended", False)
                if isinstance(is_recommended, str):
                    is_recommended = is_recommended.lower() in ["true", "1", "yes"]

                # 生成 slug
                slug = generate_slug(title, db)

                # 创建文章
                new_post = Post(
                    column_id=column_id,
                    title=title,
                    slug=slug,
                    summary=summary,
                    content_markdown=content,
                    content_html=content_html,
                    status=article_status,
                    is_recommended=is_recommended,
                    is_pinned=False,
                    view_count=0,
                )

                db.add(new_post)
                db.flush()

                imported += 1

            except Exception as e:
                errors.append(f"第 {i+1} 篇失败: {str(e)}")
                continue

        db.commit()

        # 触发静态页面生成（如果有发布的文章）
        if any(a.get("status") == "published" for a in articles):
            background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": "导入完成",
                "data": {
                    "imported": imported,
                    "skipped": skipped,
                    "errors": errors
                }
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"导入失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/delete", response_class=JSONResponse)
async def batch_delete_posts(
    request: Request,
    db: Session = Depends(get_db),
):
    """批量删除文章（移到回收站）"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])

        if not post_ids or not isinstance(post_ids, list):
            return JSONResponse(
                content={"success": False, "message": "无效的文章ID列表"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 批量软删除
        db.query(Post).filter(Post.id.in_(post_ids)).update(
            {"status": "trashed", "updated_at": func.now()},
            synchronize_session=False
        )
        db.commit()

        return JSONResponse(
            content={
                "success": True,
                "message": f"成功删除 {len(post_ids)} 篇文章，已移到回收站"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ========== 回收站功能 ==========

@router.get("/trash", response_class=HTMLResponse)
async def list_trashed_posts(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
):
    """
    回收站 - 已删除文章列表
    """
    from datetime import datetime

    # 基础查询 - 只查询已删除的文章
    query = db.query(Post).options(
        joinedload(Post.column),
        joinedload(Post.categories),
    ).filter(Post.status == "trashed")

    # 排序: 按删除时间倒序
    query = query.order_by(Post.updated_at.desc())

    # 分页
    page_size = 20
    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    offset = (page - 1) * page_size
    posts = query.limit(page_size).offset(offset).all()

    return templates.TemplateResponse(
        "posts/trash.html",
        {
            "request": request,
            "posts": posts,
            "page": page,
            "total_pages": total_pages,
            "total": total,
            "now": datetime.now(),
        },
    )


@router.post("/trash/{post_id}/restore", response_class=JSONResponse)
async def restore_trashed_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    """
    恢复已删除的文章
    """
    try:
        post = db.query(Post).filter(Post.id == post_id, Post.status == "trashed").first()
        if not post:
            return JSONResponse(
                content={"success": False, "message": "文章不存在或未被删除"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # 恢复为草稿状态
        post.status = "draft"
        db.commit()

        return JSONResponse(
            content={"success": True, "message": "文章已恢复到草稿箱"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"恢复失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/restore", response_class=JSONResponse)
async def batch_restore_posts(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    批量恢复文章
    """
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])

        if not post_ids or not isinstance(post_ids, list):
            return JSONResponse(
                content={"success": False, "message": "无效的文章ID列表"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 恢复所有选中的文章
        count = db.query(Post).filter(
            Post.id.in_(post_ids),
            Post.status == "trashed"
        ).update(
            {"status": "draft", "updated_at": func.now()},
            synchronize_session=False
        )
        db.commit()

        return JSONResponse(
            content={
                "success": True,
                "message": f"成功恢复 {count} 篇文章"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"恢复失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/permanent-delete", response_class=JSONResponse)
async def batch_permanent_delete_posts(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    批量永久删除文章
    """
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])

        if not post_ids or not isinstance(post_ids, list):
            return JSONResponse(
                content={"success": False, "message": "无效的文章ID列表"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 获取要删除的文章
        posts = db.query(Post).filter(
            Post.id.in_(post_ids),
            Post.status == "trashed"
        ).all()

        count = 0
        for post in posts:
            # 清除分类关联
            post.categories = []
            db.delete(post)
            count += 1

        db.commit()

        return JSONResponse(
            content={
                "success": True,
                "message": f"已永久删除 {count} 篇文章"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/trash/{post_id}/permanent-delete", response_class=JSONResponse)
async def permanent_delete_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    """
    永久删除文章（不可恢复）
    """
    try:
        post = db.query(Post).filter(Post.id == post_id, Post.status == "trashed").first()
        if not post:
            return JSONResponse(
                content={"success": False, "message": "文章不存在或未被删除"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # 先清除分类关联
        post.categories = []

        # 永久删除
        db.delete(post)
        db.commit()

        return JSONResponse(
            content={"success": True, "message": "文章已永久删除"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/trash/empty", response_class=JSONResponse)
async def empty_trash(
    db: Session = Depends(get_db),
):
    """
    清空回收站（永久删除所有已删除的文章）
    """
    try:
        # 获取所有已删除的文章
        trashed_posts = db.query(Post).filter(Post.status == "trashed").all()

        count = 0
        for post in trashed_posts:
            # 清除分类关联
            post.categories = []
            db.delete(post)
            count += 1

        db.commit()

        return JSONResponse(
            content={"success": True, "message": f"已永久删除 {count} 篇文章"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"清空失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ============================================================
# 版本历史 API
# ============================================================


@router.get("/{post_id}/versions", response_class=JSONResponse)
async def get_post_versions(
    post_id: int,
    db: Session = Depends(get_db),
):
    """获取文章版本历史"""
    from app.models import ContentVersion

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    versions = db.query(ContentVersion).filter(
        ContentVersion.content_type == "post",
        ContentVersion.content_id == post_id
    ).order_by(ContentVersion.version_number.desc()).all()

    return JSONResponse(
        content={
            "success": True,
            "data": {
                "post_id": post_id,
                "post_title": post.title,
                "versions": [v.to_dict() for v in versions]
            }
        }
    )


@router.post("/{post_id}/versions/{version_id}/restore", response_class=JSONResponse)
async def restore_post_version(
    post_id: int,
    version_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """恢复到指定版本"""
    from app.models import ContentVersion
    import json

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    version = db.query(ContentVersion).filter(
        ContentVersion.id == version_id,
        ContentVersion.content_type == "post",
        ContentVersion.content_id == post_id
    ).first()

    if not version:
        return JSONResponse(
            content={"success": False, "message": "版本不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    try:
        # 解析快照
        snapshot = json.loads(version.content_snapshot) if version.content_snapshot else {}

        # 恢复内容
        if "title" in snapshot:
            post.title = snapshot["title"]
        if "summary" in snapshot:
            post.summary = snapshot.get("summary")
        if "content_markdown" in snapshot:
            post.content_markdown = snapshot.get("content_markdown")
        if "content_html" in snapshot:
            post.content_html = snapshot.get("content_html")

        post.updated_at = func.now()
        db.commit()

        # 生成静态页面
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"已恢复到版本 #{version.version_number}"
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"恢复失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def save_content_version(
    db: Session,
    content_type: str,
    content_id: int,
    action: str,
    title: str,
    snapshot: dict,
    admin_id: int = None,
    admin_name: str = None,
    remark: str = None
):
    """保存内容版本（辅助函数）"""
    from app.models import ContentVersion

    # 获取当前最大版本号
    last_version = db.query(ContentVersion).filter(
        ContentVersion.content_type == content_type,
        ContentVersion.content_id == content_id
    ).order_by(ContentVersion.version_number.desc()).first()

    version_number = (last_version.version_number if last_version else 0) + 1

    version = ContentVersion(
        content_type=content_type,
        content_id=content_id,
        version_number=version_number,
        title=title,
        content_snapshot=json.dumps(snapshot, ensure_ascii=False) if snapshot else None,
        action=action,
        admin_id=admin_id,
        admin_name=admin_name,
        remark=remark
    )

    db.add(version)
    db.commit()

    return version


@router.post("/batch/duplicate", response_class=JSONResponse)
async def batch_duplicate_posts(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """批量复制文章"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])

        if not post_ids:
            return JSONResponse(
                content={"success": False, "message": "请选择文章"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        from app.services.post_service import generate_slug as post_generate_slug

        duplicated_count = 0

        for post_id in post_ids:
            post = db.query(Post).filter(Post.id == post_id).first()
            if not post:
                continue

            # 生成新的 slug
            new_slug = post_generate_slug(post.title + "-copy", db)

            # 复制文章
            new_post = Post(
                column_id=post.column_id,
                title=post.title + " (副本)",
                title_en=post.title_en + " (Copy)" if post.title_en else None,
                slug=new_slug,
                summary=post.summary,
                summary_en=post.summary_en,
                cover_media_id=post.cover_media_id,
                content_markdown=post.content_markdown,
                content_markdown_en=post.content_markdown_en,
                content_html=post.content_html,
                content_html_en=post.content_html_en,
                status="draft",  # 复制的文章默认为草稿
                is_recommended=False,
                is_pinned=False,
            )
            db.add(new_post)
            db.flush()

            # 复制分类
            new_post.categories = post.categories[:]

            duplicated_count += 1

        db.commit()

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"成功复制 {duplicated_count} 篇文章（已设为草稿状态）"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"复制失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/edit", response_class=JSONResponse)
async def batch_edit_posts(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """批量编辑文章（修改多个字段）"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])
        updates = data.get("updates", {})

        if not post_ids:
            return JSONResponse(
                content={"success": False, "message": "请选择文章"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not updates:
            return JSONResponse(
                content={"success": False, "message": "请指定要修改的字段"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 构建更新字典
        update_fields = {}
        update_values = {}

        # 状态
        if "status" in updates:
            valid_statuses = ["draft", "published", "offline"]
            if updates["status"] not in valid_statuses:
                return JSONResponse(
                    content={"success": False, "message": f"无效的状态值: {updates['status']}"},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            update_fields["status"] = updates["status"]
            update_values["status"] = updates["status"]

        # 栏目
        if "column_id" in updates:
            column_id = updates["column_id"]
            # 验证栏目是否存在
            column = db.query(SiteColumn).filter(SiteColumn.id == column_id).first()
            if not column:
                return JSONResponse(
                    content={"success": False, "message": "目标栏目不存在"},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            update_fields["column_id"] = column_id
            update_values["column_id"] = column_id

        # 推荐
        if "is_recommended" in updates:
            update_fields["is_recommended"] = updates["is_recommended"]
            update_values["is_recommended"] = updates["is_recommended"]

        # 置顶
        if "is_pinned" in updates:
            update_fields["is_pinned"] = updates["is_pinned"]
            update_values["is_pinned"] = updates["is_pinned"]

        # 浏览量重置
        if "view_count" in updates and updates["view_count"] == 0:
            update_fields["view_count"] = 0
            update_values["view_count"] = 0

        if not update_fields:
            return JSONResponse(
                content={"success": False, "message": "没有有效的更新字段"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 添加更新时间
        update_fields["updated_at"] = func.now()
        update_values["updated_at"] = func.now()

        # 执行批量更新
        count = db.query(Post).filter(Post.id.in_(post_ids)).update(
            update_fields,
            synchronize_session=False
        )
        db.commit()

        # 生成修改字段描述
        field_descriptions = []
        if "status" in update_values:
            status_map = {"draft": "草稿", "published": "已发布", "offline": "已下线"}
            field_descriptions.append(f"状态改为「{status_map.get(update_values['status'], update_values['status'])}」")
        if "column_id" in update_values:
            field_descriptions.append("栏目")
        if "is_recommended" in update_values:
            field_descriptions.append("推荐状态" if update_values["is_recommended"] else "取消推荐")
        if "is_pinned" in update_values:
            field_descriptions.append("置顶状态" if update_values["is_pinned"] else "取消置顶")
        if "view_count" in update_values:
            field_descriptions.append("浏览量重置")

        field_desc_str = "、".join(field_descriptions)

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"成功批量编辑 {count} 篇文章，修改了：{field_desc_str}"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"编辑失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/delete", response_class=JSONResponse)
async def batch_delete_posts(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """批量删除文章（移至回收站）"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])

        if not post_ids:
            return JSONResponse(
                content={"success": False, "message": "请选择文章"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 将状态改为 draft（视为移至回收站/草稿箱）
        count = db.query(Post).filter(Post.id.in_(post_ids)).update(
            {"status": "draft", "updated_at": func.now()},
            synchronize_session=False
        )
        db.commit()

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"已成功将 {count} 篇文章移至回收站"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ========== 内容审核功能 ==========

@router.post("/{post_id}/approve", response_class=JSONResponse)
async def approve_post(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """审核通过文章"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    post.is_approved = 1  # 已审核通过
    db.commit()

    return JSONResponse(
        content={"success": True, "message": "审核通过"}
    )


@router.post("/{post_id}/reject", response_class=JSONResponse)
async def reject_post(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """驳回文章"""
    from pydantic import BaseModel

    class RejectRequest(BaseModel):
        reason: str = ""

    data = await request.json()
    reject_data = RejectRequest(**data)

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    post.is_approved = -1  # 已驳回
    post.admin_reply = reject_data.reason
    db.commit()

    return JSONResponse(
        content={"success": True, "message": "已驳回"}
    )


@router.get("/pending-approval", response_class=HTMLResponse)
async def pending_approval_list(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
):
    """待审核文章列表"""
    query = db.query(Post).options(
        joinedload(Post.column),
    ).filter(
        Post.is_approved == 0  # 待审核
    ).order_by(Post.created_at.desc())

    page_size = 20
    total = query.count()
    posts = query.limit(page_size).offset((page - 1) * page_size).all()

    return templates.TemplateResponse(
        "posts/pending_approval.html",
        {
            "request": request,
            "posts": posts,
            "page": page,
            "total_pages": (total + page_size - 1) // page_size,
            "total": total,
        },
    )


@router.get("/api/pending-approval/count")
async def get_pending_approval_count(
    db: Session = Depends(get_db),
):
    """获取待审核文章数量"""
    count = db.query(Post).filter(Post.is_approved == 0).count()
    return JSONResponse(content={"success": True, "count": count})


# ========== 定时发布功能 ==========

@router.post("/{post_id}/schedule", response_class=JSONResponse)
async def schedule_post(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """设置定时发布"""
    from datetime import datetime

    class ScheduleRequest(BaseModel):
        scheduled_at: str  # ISO format datetime string

    data = await request.json()
    schedule_data = ScheduleRequest(**data)

    try:
        scheduled_time = datetime.fromisoformat(schedule_data.scheduled_at.replace("Z", "+00:00"))
    except ValueError:
        return JSONResponse(
            content={"success": False, "message": "时间格式无效，请使用 ISO 格式"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    post.scheduled_at = scheduled_time
    post.status = "draft"  # 定时发布的文章保持草稿状态
    db.commit()

    return JSONResponse(
        content={
            "success": True,
            "message": f"已设置为 {scheduled_time.strftime('%Y-%m-%d %H:%M')} 发布"
        }
    )


@router.post("/{post_id}/cancel-schedule", response_class=JSONResponse)
async def cancel_schedule(
    post_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """取消定时发布"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    post.scheduled_at = None
    db.commit()

    return JSONResponse(
        content={"success": True, "message": "已取消定时发布"}
    )


@router.post("/batch/publish", response_class=JSONResponse)
async def batch_publish_scheduled(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """批量立即发布定时文章"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])

        if not post_ids or not isinstance(post_ids, list):
            return JSONResponse(
                content={"success": False, "message": "无效的文章ID列表"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        count = db.query(Post).filter(
            Post.id.in_(post_ids),
            Post.scheduled_at.isnot(None)
        ).update(
            {"status": "published", "scheduled_at": None, "updated_at": func.now()},
            synchronize_session=False
        )
        db.commit()

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"成功发布 {count} 篇文章"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"发布失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/cancel-schedule", response_class=JSONResponse)
async def batch_cancel_schedule(
    request: Request,
    db: Session = Depends(get_db),
):
    """批量取消定时发布"""
    try:
        data = await request.json()
        post_ids = data.get("post_ids", [])

        if not post_ids or not isinstance(post_ids, list):
            return JSONResponse(
                content={"success": False, "message": "无效的文章ID列表"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        count = db.query(Post).filter(
            Post.id.in_(post_ids),
            Post.scheduled_at.isnot(None)
        ).update(
            {"scheduled_at": None, "updated_at": func.now()},
            synchronize_session=False
        )
        db.commit()

        return JSONResponse(
            content={
                "success": True,
                "message": f"已取消 {count} 篇定时发布"
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"取消失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/scheduled", response_class=HTMLResponse)
async def scheduled_posts_list(
    request: Request,
    db: Session = Depends(get_db),
):
    """定时发布文章列表"""
    from datetime import datetime

    now = datetime.now()

    posts = db.query(Post).options(
        joinedload(Post.column),
    ).filter(
        Post.scheduled_at != None,
        Post.scheduled_at > now
    ).order_by(Post.scheduled_at.asc()).all()

    return templates.TemplateResponse(
        "posts/scheduled.html",
        {
            "request": request,
            "posts": posts,
        },
    )


@router.get("/seo", response_class=HTMLResponse)
async def seo_analysis_page(
    request: Request,
    db: Session = Depends(get_db),
):
    """SEO 分析页面"""
    return templates.TemplateResponse(
        "posts/seo_analysis.html",
        {
            "request": request,
        },
    )


@router.get("/api/scheduled/count")
async def get_scheduled_count(
    db: Session = Depends(get_db),
):
    """获取定时发布文章数量"""
    from datetime import datetime
    now = datetime.now()
    count = db.query(Post).filter(
        Post.scheduled_at != None,
        Post.scheduled_at > now
    ).count()
    return JSONResponse(content={"success": True, "count": count})


# ========== 批量审核功能 ==========

@router.post("/batch/approve", response_class=JSONResponse)
async def batch_approve_posts(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """批量审核通过"""
    data = await request.json()
    post_ids = data.get("post_ids", [])

    if not post_ids:
        return JSONResponse(
            content={"success": False, "message": "请选择文章"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    count = db.query(Post).filter(Post.id.in_(post_ids)).update(
        {"is_approved": 1},
        synchronize_session=False
    )
    db.commit()

    return JSONResponse(
        content={
            "success": True,
            "message": f"成功审核通过 {count} 篇文章"
        }
    )


@router.post("/batch/reject", response_class=JSONResponse)
async def batch_reject_posts(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """批量驳回"""
    from pydantic import BaseModel

    class BatchRejectRequest(BaseModel):
        post_ids: list
        reason: str = ""

    data = await request.json()
    reject_data = BatchRejectRequest(**data)

    if not reject_data.post_ids:
        return JSONResponse(
            content={"success": False, "message": "请选择文章"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    count = db.query(Post).filter(Post.id.in_(reject_data.post_ids)).update(
        {"is_approved": -1, "admin_reply": reject_data.reason},
        synchronize_session=False
    )
    db.commit()

    return JSONResponse(
        content={
            "success": True,
            "message": f"已驳回 {count} 篇文章"
        }
    )


@router.post("/batch")
async def batch_posts(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """批量操作文章"""
    data = await request.json()
    action = data.get("action")
    post_ids = data.get("post_ids", [])

    if not post_ids:
        return JSONResponse(
            content={"success": False, "message": "请选择文章"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not action:
        return JSONResponse(
            content={"success": False, "message": "请指定操作类型"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    count = 0

    if action == "publish":
        count = db.query(Post).filter(Post.id.in_(post_ids)).update(
            {"status": "published"},
            synchronize_session=False
        )
        message = f"已发布 {count} 篇文章"

    elif action == "unpublish":
        count = db.query(Post).filter(Post.id.in_(post_ids)).update(
            {"status": "draft"},
            synchronize_session=False
        )
        message = f"已取消发布 {count} 篇文章"

    elif action == "delete":
        # 检查是否可以删除
        deletable_ids = []
        for pid in post_ids:
            if can_delete_post(pid, db):
                deletable_ids.append(pid)

        if not deletable_ids:
            return JSONResponse(
                content={"success": False, "message": "所选文章都不能被删除"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        count = db.query(Post).filter(Post.id.in_(deletable_ids)).delete(
            synchronize_session=False
        )
        message = f"已删除 {count} 篇文章"

    elif action == "recommended":
        count = db.query(Post).filter(Post.id.in_(post_ids)).update(
            {"is_recommended": True},
            synchronize_session=False
        )
        message = f"已将 {count} 篇文章设为推荐"

    elif action == "unrecommended":
        count = db.query(Post).filter(Post.id.in_(post_ids)).update(
            {"is_recommended": False},
            synchronize_session=False
        )
        message = f"已取消 {count} 篇推荐"

    elif action == "pinned":
        count = db.query(Post).filter(Post.id.in_(post_ids)).update(
            {"is_pinned": True},
            synchronize_session=False
        )
        message = f"已将 {count} 篇文章置顶"

    elif action == "unpinned":
        count = db.query(Post).filter(Post.id.in_(post_ids)).update(
            {"is_pinned": False},
            synchronize_session=False
        )
        message = f"已取消 {count} 篇置顶"

    elif action == "move_column":
        column_id = data.get("column_id")
        if not column_id:
            return JSONResponse(
                content={"success": False, "message": "请选择目标栏目"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        count = db.query(Post).filter(Post.id.in_(post_ids)).update(
            {"column_id": column_id},
            synchronize_session=False
        )
        message = f"已将 {count} 篇文章移动到目标栏目"

    else:
        return JSONResponse(
            content={"success": False, "message": f"不支持的操作: {action}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    db.commit()

    return JSONResponse(
        content={
            "success": True,
            "message": message,
            "count": count
        }
    )


@router.get("/batch-form")
async def batch_form(
    request: Request,
    db: Session = Depends(get_db),
):
    """批量操作表单"""
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.column_type == ColumnType.POST)
        .order_by(SiteColumn.sort_order)
        .all()
    )

    return templates.TemplateResponse(
        "posts/batch_form.html",
        {
            "request": request,
            "columns": columns,
        },
    )
