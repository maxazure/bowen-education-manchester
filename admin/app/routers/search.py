"""
全站搜索路由
"""

from typing import Optional
from sqlalchemy import or_

from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models import Post, Product, Gallery, SiteColumn

router = APIRouter(tags=["search"])


@router.get("/search", response_class=HTMLResponse)
async def search_page(
    request: Request,
    q: Optional[str] = None,
    type: Optional[str] = None,
):
    """全站搜索页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    results = []
    keyword = q or ""

    if keyword:
        db = get_db()
        try:
            if type is None or type == "post":
                posts = db.query(Post).filter(
                    or_(
                        Post.title.contains(keyword),
                        Post.summary.contains(keyword),
                        Post.content_html.contains(keyword)
                    )
                ).limit(10).all()
                for p in posts:
                    results.append({
                        "type": "post",
                        "title": p.title,
                        "url": f"/admin/posts/{p.id}/edit",
                        "summary": p.summary[:100] if p.summary else "",
                        "status": p.status,
                        "updated_at": p.updated_at.strftime('%Y-%m-%d') if p.updated_at else "",
                    })

            if type is None or type == "product":
                products = db.query(Product).filter(
                    or_(
                        Product.name.contains(keyword),
                        Product.description.contains(keyword)
                    )
                ).limit(10).all()
                for p in products:
                    results.append({
                        "type": "product",
                        "title": p.name,
                        "url": f"/admin/products/{p.id}/edit",
                        "summary": p.description[:100] if p.description else "",
                        "status": p.status,
                        "updated_at": p.updated_at.strftime('%Y-%m-%d') if p.updated_at else "",
                    })

            if type is None or type == "gallery":
                galleries = db.query(Gallery).filter(
                    or_(
                        Gallery.title.contains(keyword),
                        Gallery.description.contains(keyword)
                    )
                ).limit(10).all()
                for g in galleries:
                    results.append({
                        "type": "gallery",
                        "title": g.title,
                        "url": f"/admin/galleries/{g.id}/edit",
                        "summary": g.description[:100] if g.description else "",
                        "status": g.status,
                        "updated_at": g.updated_at.strftime('%Y-%m-%d') if g.updated_at else "",
                    })
        finally:
            db.close()

    return templates.TemplateResponse("search.html", {
        "request": request,
        "results": results,
        "keyword": keyword,
        "search_type": type,
    })


@router.get("/api/search")
async def search_api(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    types: Optional[str] = Query("post,product,gallery", description="搜索类型，逗号分隔"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """全站搜索 API"""
    results = []
    type_list = [t.strip() for t in types.split(",")]
    search_types = set(type_list)

    if "post" in search_types:
        posts = db.query(Post).filter(
            or_(
                Post.title.contains(q),
                Post.summary.contains(q),
                Post.slug.contains(q)
            )
        ).limit(limit).all()
        for p in posts:
            results.append({
                "type": "post",
                "id": p.id,
                "title": p.title,
                "url": f"/admin/posts/{p.id}/edit",
                "summary": p.summary[:100] if p.summary else "",
                "status": p.status,
            })

    if "product" in search_types and len(results) < limit:
        remaining = limit - len(results)
        products = db.query(Product).filter(
            or_(
                Product.name.contains(q),
                Product.description.contains(q),
                Product.slug.contains(q)
            )
        ).limit(remaining).all()
        for p in products:
            results.append({
                "type": "product",
                "id": p.id,
                "title": p.name,
                "url": f"/admin/products/{p.id}/edit",
                "summary": p.description[:100] if p.description else "",
                "status": p.status,
            })

    if "gallery" in search_types and len(results) < limit:
        remaining = limit - len(results)
        galleries = db.query(Gallery).filter(
            or_(
                Gallery.title.contains(q),
                Gallery.description.contains(q)
            )
        ).limit(remaining).all()
        for g in galleries:
            results.append({
                "type": "gallery",
                "id": g.id,
                "title": g.title,
                "url": f"/admin/galleries/{g.id}/edit",
                "summary": g.description[:100] if g.description else "",
                "status": g.status,
            })

    return JSONResponse(content={
        "success": True,
        "results": results,
        "total": len(results),
        "keyword": q,
    })


@router.get("/api/quick-search")
async def quick_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    """快速搜索（用于搜索框自动完成）"""
    results = []

    # 搜索文章
    posts = db.query(Post).filter(
        Post.title.contains(q)
    ).limit(limit).all()
    for p in posts:
        results.append({
            "type": "post",
            "id": p.id,
            "title": p.title,
            "url": f"/admin/posts/{p.id}/edit",
            "icon": "bi-file-earmark-text",
            "color": "primary",
        })

    # 搜索产品
    if len(results) < limit:
        remaining = limit - len(results)
        products = db.query(Product).filter(
            Product.name.contains(q)
        ).limit(remaining).all()
        for p in products:
            results.append({
                "type": "product",
                "id": p.id,
                "title": p.name,
                "url": f"/admin/products/{p.id}/edit",
                "icon": "bi-box-seam",
                "color": "success",
            })

    return JSONResponse(content={
        "success": True,
        "data": results
    })
