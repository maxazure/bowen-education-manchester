"""
单页管理路由

提供单页的 CRUD 操作和发布管理
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.site import SinglePage, SiteColumn
from app.services import single_page_service

router = APIRouter(prefix="/pages", tags=["pages"])
templates = Jinja2Templates(directory="admin/templates")


@router.get("", response_class=HTMLResponse)
async def list_pages(request: Request, db: Session = Depends(get_db)):
    """
    单页列表页面

    显示所有单页及其状态

    Args:
        request: FastAPI request 对象
        db: 数据库会话

    Returns:
        单页列表页面 HTML
    """
    # 获取所有单页
    pages = db.query(SinglePage).order_by(SinglePage.created_at.desc()).all()

    return templates.TemplateResponse(
        "pages/list.html",
        {
            "request": request,
            "pages": pages,
        },
    )


@router.get("/new", response_class=HTMLResponse)
async def new_page_form(request: Request, db: Session = Depends(get_db)):
    """
    新建单页表单页面

    Args:
        request: FastAPI request 对象
        db: 数据库会话

    Returns:
        新建单页表单页面 HTML
    """
    # 获取所有栏目（用于选择关联栏目）
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.is_enabled.is_(True))
        .order_by(SiteColumn.sort_order)
        .all()
    )

    return templates.TemplateResponse(
        "pages/form.html",
        {
            "request": request,
            "page": None,
            "columns": columns,
            "mode": "create",
        },
    )


@router.post("")
async def create_page(
    request: Request,
    column_id: int = Form(...),
    title: str = Form(...),
    slug: Optional[str] = Form(None),
    subtitle: Optional[str] = Form(None),
    content_markdown: str = Form(...),
    hero_media_id: Optional[int] = Form(None),
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    seo_keywords: Optional[str] = Form(None),
    status: str = Form("draft"),
    db: Session = Depends(get_db),
):
    """
    创建单页

    Args:
        request: FastAPI request 对象
        column_id: 栏目 ID
        title: 页面标题
        slug: URL Slug
        subtitle: 副标题
        content_markdown: Markdown 内容
        hero_media_id: Hero 背景图 ID
        seo_title: SEO 标题
        seo_description: SEO 描述
        seo_keywords: SEO 关键词
        status: 状态 (draft/published)
        db: 数据库会话

    Returns:
        重定向到列表页面或返回错误
    """
    try:
        # 生成 slug (如果未提供)
        if not slug:
            slug = single_page_service.generate_slug(title, db)
        else:
            # 验证 slug 唯一性
            existing = db.query(SinglePage).filter(SinglePage.slug == slug).first()
            if existing:
                raise HTTPException(status_code=400, detail="Slug 已存在")

        # 转换 Markdown 为 HTML
        content_html = single_page_service.markdown_to_html(content_markdown)

        # 创建单页
        page = SinglePage(
            column_id=column_id,
            title=title,
            slug=slug,
            subtitle=subtitle,
            content_markdown=content_markdown,
            content_html=content_html,
            hero_media_id=hero_media_id if hero_media_id else None,
            seo_title=seo_title,
            seo_description=seo_description,
            seo_keywords=seo_keywords,
            status=status,
            published_at=datetime.now() if status == "published" else None,
        )

        db.add(page)
        db.commit()
        db.refresh(page)

        return RedirectResponse(
            url="/admin/pages",
            status_code=303,
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{page_id}/edit", response_class=HTMLResponse)
async def edit_page_form(request: Request, page_id: int, db: Session = Depends(get_db)):
    """
    编辑单页表单页面

    Args:
        request: FastAPI request 对象
        page_id: 页面 ID
        db: 数据库会话

    Returns:
        编辑单页表单页面 HTML
    """
    page = db.query(SinglePage).filter(SinglePage.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="页面不存在")

    # 获取所有栏目
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.is_enabled.is_(True))
        .order_by(SiteColumn.sort_order)
        .all()
    )

    return templates.TemplateResponse(
        "pages/form.html",
        {
            "request": request,
            "page": page,
            "columns": columns,
            "mode": "edit",
        },
    )


@router.post("/{page_id}")
async def update_page(
    request: Request,
    page_id: int,
    column_id: int = Form(...),
    title: str = Form(...),
    slug: str = Form(...),
    subtitle: Optional[str] = Form(None),
    content_markdown: str = Form(...),
    hero_media_id: Optional[int] = Form(None),
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    seo_keywords: Optional[str] = Form(None),
    status: str = Form("draft"),
    db: Session = Depends(get_db),
):
    """
    更新单页

    Args:
        request: FastAPI request 对象
        page_id: 页面 ID
        ... (其他字段同创建)
        db: 数据库会话

    Returns:
        重定向到列表页面或返回错误
    """
    try:
        page = db.query(SinglePage).filter(SinglePage.id == page_id).first()
        if not page:
            raise HTTPException(status_code=404, detail="页面不存在")

        # 验证 slug 唯一性 (排除当前页面)
        existing = (
            db.query(SinglePage)
            .filter(SinglePage.slug == slug, SinglePage.id != page_id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="Slug 已存在")

        # 转换 Markdown 为 HTML
        content_html = single_page_service.markdown_to_html(content_markdown)

        # 更新字段
        page.column_id = column_id
        page.title = title
        page.slug = slug
        page.subtitle = subtitle
        page.content_markdown = content_markdown
        page.content_html = content_html
        page.hero_media_id = hero_media_id if hero_media_id else None
        page.seo_title = seo_title
        page.seo_description = seo_description
        page.seo_keywords = seo_keywords

        # 如果状态从 draft 变为 published,设置发布时间
        if page.status == "draft" and status == "published":
            page.published_at = datetime.now()

        page.status = status

        db.commit()
        db.refresh(page)

        return RedirectResponse(
            url="/admin/pages",
            status_code=303,
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{page_id}")
async def delete_page(page_id: int, db: Session = Depends(get_db)):
    """
    删除单页

    Args:
        page_id: 页面 ID
        db: 数据库会话

    Returns:
        JSON 响应
    """
    try:
        # 检查是否可以删除
        can_delete, error_msg = single_page_service.can_delete_page(db, page_id)
        if not can_delete:
            return JSONResponse(
                status_code=400, content={"success": False, "message": error_msg}
            )

        page = db.query(SinglePage).filter(SinglePage.id == page_id).first()
        if not page:
            return JSONResponse(
                status_code=404, content={"success": False, "message": "页面不存在"}
            )

        db.delete(page)
        db.commit()

        return JSONResponse(content={"success": True, "message": "删除成功"})

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500, content={"success": False, "message": str(e)}
        )


@router.post("/{page_id}/publish")
async def toggle_publish(page_id: int, db: Session = Depends(get_db)):
    """
    发布/取消发布单页

    Args:
        page_id: 页面 ID
        db: 数据库会话

    Returns:
        JSON 响应
    """
    try:
        page = db.query(SinglePage).filter(SinglePage.id == page_id).first()
        if not page:
            return JSONResponse(
                status_code=404, content={"success": False, "message": "页面不存在"}
            )

        # 切换状态
        if page.status == "published":
            success, message = single_page_service.unpublish_page(db, page_id)
        else:
            success, message = single_page_service.publish_page(db, page_id)

        if not success:
            return JSONResponse(
                status_code=400, content={"success": False, "message": message}
            )

        # 刷新获取最新状态
        db.refresh(page)

        return JSONResponse(
            content={"success": True, "message": message, "status": page.status}
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500, content={"success": False, "message": str(e)}
        )
