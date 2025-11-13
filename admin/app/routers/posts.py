"""
文章管理路由
"""

import math
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.post import Post, PostCategory
from app.models.site import ColumnType, SiteColumn
from app.services.post_service import (can_delete_post, generate_slug,
                                       publish_post, unpublish_post)
from app.services.single_page_service import markdown_to_html

router = APIRouter(prefix="/posts", tags=["posts"])

templates = Jinja2Templates(directory="admin/templates")


@router.get("", response_class=HTMLResponse)
async def list_posts(
    request: Request,
    db: Session = Depends(get_db),
    column_id: Optional[int] = None,
    category: Optional[str] = None,
    status_filter: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
):
    """
    文章列表页

    支持筛选: column_id, category, status, keyword, page
    """
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

    # 排序: 置顶文章优先,然后按更新时间
    query = query.order_by(Post.is_pinned.desc(), Post.updated_at.desc())

    # 分页
    page_size = 20
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
            "page": page,
            "total_pages": total_pages,
            "total": total,
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
            "action": "/admin/posts",
            "method": "POST",
        },
    )


@router.post("", response_class=JSONResponse)
async def create_post(
    request: Request,
    db: Session = Depends(get_db),
    column_id: int = Form(...),
    title: str = Form(...),
    slug: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    content_markdown: Optional[str] = Form(None),
    cover_media_id: Optional[int] = Form(None),
    category_ids: str = Form(""),  # 逗号分隔的分类 ID
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    is_recommended: bool = Form(False),
    is_pinned: bool = Form(False),
    status: str = Form("draft"),
):
    """创建文章"""
    try:
        # 生成 slug
        if not slug:
            slug = generate_slug(title, db)

        # 转换 Markdown 为 HTML
        content_html = ""
        if content_markdown:
            content_html = markdown_to_html(content_markdown)

        # 创建文章
        post = Post(
            column_id=column_id,
            title=title,
            slug=slug,
            summary=summary,
            content_markdown=content_markdown,
            content_html=content_html,
            cover_media_id=cover_media_id,
            seo_title=seo_title,
            seo_description=seo_description,
            is_recommended=is_recommended,
            is_pinned=is_pinned,
            status=status,
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
    db: Session = Depends(get_db),
    column_id: int = Form(...),
    title: str = Form(...),
    slug: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    content_markdown: Optional[str] = Form(None),
    cover_media_id: Optional[int] = Form(None),
    category_ids: str = Form(""),
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    is_recommended: bool = Form(False),
    is_pinned: bool = Form(False),
    status: str = Form("draft"),
):
    """更新文章"""
    try:
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(status_code=404, detail="文章不存在")

        # 更新 slug
        if not slug:
            slug = generate_slug(title, db, exclude_id=post_id)

        # 转换 Markdown 为 HTML
        content_html = post.content_html
        if content_markdown:
            content_html = markdown_to_html(content_markdown)

        # 更新字段
        post.column_id = column_id
        post.title = title
        post.slug = slug
        post.summary = summary
        post.content_markdown = content_markdown
        post.content_html = content_html
        post.cover_media_id = cover_media_id
        post.seo_title = seo_title
        post.seo_description = seo_description
        post.is_recommended = is_recommended
        post.is_pinned = is_pinned
        post.status = status

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
    db: Session = Depends(get_db),
):
    """删除文章"""
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

        db.delete(post)
        db.commit()

        return JSONResponse(
            content={"success": True, "message": "文章删除成功"},
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
