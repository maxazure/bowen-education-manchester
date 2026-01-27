"""
高级搜索路由
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy import or_, and_, func, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import Post, Product, Gallery, SiteColumn, MediaFile, Contact, Comment

router = APIRouter(tags=["advanced-search"])


class SearchFilters(BaseModel):
    """搜索筛选参数"""
    keyword: str = ""
    content_type: Optional[List[str]] = []
    status: Optional[List[str]] = []
    column_ids: Optional[List[int]] = []
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    has_image: Optional[bool] = None
    is_recommended: Optional[bool] = None
    is_pinned: Optional[bool] = None


@router.get("/advanced-search", response_class=HTMLResponse)
async def advanced_search_page(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """高级搜索页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 获取栏目列表
    columns = db.query(SiteColumn).order_by(SiteColumn.sort_order).all()

    # 获取统计信息
    stats = {
        "posts_total": db.query(func.count(Post.id)).scalar() or 0,
        "products_total": db.query(func.count(Product.id)).scalar() or 0,
        "galleries_total": db.query(func.count(Gallery.id)).scalar() or 0,
        "media_total": db.query(func.count(MediaFile.id)).scalar() or 0,
    }

    return templates.TemplateResponse("advanced_search.html", {
        "request": request,
        "columns": columns,
        "stats": stats,
    })


@router.post("/api/advanced-search")
async def advanced_search(
    request: Request,
    filters: SearchFilters,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """高级搜索API"""
    results = {
        "posts": {"items": [], "total": 0},
        "products": {"items": [], "total": 0},
        "galleries": {"items": [], "total": 0},
        "media": {"items": [], "total": 0},
    }

    # 搜索文章
    if not filters.content_type or "post" in filters.content_type:
        post_query = db.query(Post).options(
            joinedload(Post.column),
        )

        # 关键词搜索
        if filters.keyword:
            post_query = post_query.filter(
                or_(
                    Post.title.contains(filters.keyword),
                    Post.summary.contains(filters.keyword),
                    Post.content_html.contains(filters.keyword),
                    Post.slug.contains(filters.keyword),
                )
            )

        # 状态筛选
        if filters.status:
            post_query = post_query.filter(Post.status.in_(filters.status))

        # 栏目筛选
        if filters.column_ids:
            post_query = post_query.filter(Post.column_id.in_(filters.column_ids))

        # 日期筛选
        if filters.date_from:
            try:
                date_from = datetime.strptime(filters.date_from, "%Y-%m-%d")
                post_query = post_query.filter(Post.created_at >= date_from)
            except ValueError:
                pass

        if filters.date_to:
            try:
                date_to = datetime.strptime(filters.date_to, "%Y-%m-%d")
                date_to = date_to.replace(hour=23, minute=59, second=59)
                post_query = post_query.filter(Post.created_at <= date_to)
            except ValueError:
                pass

        # 推荐/置顶
        if filters.is_recommended is not None:
            post_query = post_query.filter(Post.is_recommended == filters.is_recommended)

        if filters.is_pinned is not None:
            post_query = post_query.filter(Post.is_pinned == filters.is_pinned)

        # 统计总数
        results["posts"]["total"] = post_query.count()

        # 分页
        results["posts"]["items"] = [
            {
                "id": p.id,
                "title": p.title,
                "title_en": p.title_en,
                "status": p.status,
                "column_name": p.column.name if p.column else None,
                "is_recommended": p.is_recommended,
                "is_pinned": p.is_pinned,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "updated_at": p.updated_at.isoformat() if p.updated_at else None,
                "url": f"/admin/posts/{p.id}/edit",
            }
            for p in post_query.order_by(desc(Post.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        ]

    # 搜索产品
    if not filters.content_type or "product" in filters.content_type:
        product_query = db.query(Product)

        if filters.keyword:
            product_query = product_query.filter(
                or_(
                    Product.name.contains(filters.keyword),
                    Product.description.contains(filters.keyword),
                    Product.slug.contains(filters.keyword),
                )
            )

        if filters.status:
            product_query = product_query.filter(Product.status.in_(filters.status))

        results["products"]["total"] = product_query.count()
        results["products"]["items"] = [
            {
                "id": p.id,
                "name": p.name,
                "name_en": p.name_en,
                "status": p.status,
                "price": p.price,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "url": f"/admin/products/{p.id}/edit",
            }
            for p in product_query.order_by(desc(Product.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        ]

    # 搜索相册
    if not filters.content_type or "gallery" in filters.content_type:
        gallery_query = db.query(Gallery)

        if filters.keyword:
            gallery_query = gallery_query.filter(
                or_(
                    Gallery.title.contains(filters.keyword),
                    Gallery.description.contains(filters.keyword),
                )
            )

        if filters.status:
            gallery_query = gallery_query.filter(Gallery.status.in_(filters.status))

        results["galleries"]["total"] = gallery_query.count()
        results["galleries"]["items"] = [
            {
                "id": g.id,
                "title": g.title,
                "status": g.status,
                "image_count": len(g.images) if hasattr(g, 'images') else 0,
                "created_at": g.created_at.isoformat() if g.created_at else None,
                "url": f"/admin/galleries/{g.id}/edit",
            }
            for g in gallery_query.order_by(desc(Gallery.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        ]

    # 计算总结果数
    total_results = sum(r["total"] for r in results.values())

    return JSONResponse(content={
        "success": True,
        "data": {
            "results": results,
            "total": total_results,
            "page": page,
            "page_size": page_size,
            "filters": filters.model_dump(),
        }
    })


@router.get("/api/search/suggestions")
async def search_suggestions(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """搜索建议（自动完成）"""
    suggestions = []

    # 文章标题建议
    posts = db.query(Post.title).filter(
        Post.title.contains(q)
    ).limit(limit).all()
    for p in posts:
        suggestions.append({
            "type": "post",
            "text": p.title,
            "icon": "bi-file-earmark-text",
        })

    # 产品名称建议
    if len(suggestions) < limit:
        products = db.query(Product.name).filter(
            Product.name.contains(q)
        ).limit(limit - len(suggestions)).all()
        for p in products:
            suggestions.append({
                "type": "product",
                "text": p.name,
                "icon": "bi-box-seam",
            })

    # 栏目建议
    if len(suggestions) < limit:
        columns = db.query(SiteColumn.name).filter(
            SiteColumn.name.contains(q)
        ).limit(limit - len(suggestions)).all()
        for c in columns:
            suggestions.append({
                "type": "column",
                "text": c.name,
                "icon": "bi-folder",
            })

    return JSONResponse(content={
        "success": True,
        "data": suggestions[:limit]
    })


@router.get("/api/search/history")
async def get_search_history(
    limit: int = Query(20, ge=1, le=100),
    admin_user=Depends(get_current_admin_user),
):
    """获取搜索历史"""
    # 从本地存储读取搜索历史
    return JSONResponse(content={
        "success": True,
        "data": {
            "history": []  # 前端实现本地存储
        }
    })


@router.post("/api/search/history")
async def save_search_history(
    request: Request,
    admin_user=Depends(get_current_admin_user),
):
    """保存搜索历史"""
    data = await request.json()
    keyword = data.get("keyword", "").strip()

    if not keyword:
        return JSONResponse(
            content={"success": False, "message": "关键词不能为空"},
            status_code=400
        )

    return JSONResponse(content={
        "success": True,
        "message": "搜索历史已保存"
    })


@router.delete("/api/search/history")
async def clear_search_history(
    admin_user=Depends(get_current_admin_user),
):
    """清除搜索历史"""
    return JSONResponse(content={
        "success": True,
        "message": "搜索历史已清除"
    })


@router.get("/api/search/facets")
async def get_search_facets(
    keyword: str = "",
    db: Session = Depends(get_db),
):
    """获取搜索 facets（用于筛选统计）"""
    # 按状态统计文章
    post_status_facet = db.query(
        Post.status,
        func.count(Post.id)
    ).group_by(Post.status).all()

    # 按栏目统计文章
    post_column_facet = db.query(
        SiteColumn.name,
        func.count(Post.id)
    ).join(Post).group_by(SiteColumn.id).all()

    # 按状态统计产品
    product_status_facet = db.query(
        Product.status,
        func.count(Product.id)
    ).group_by(Product.status).all()

    return JSONResponse(content={
        "success": True,
        "data": {
            "post_status": [{"status": s, "count": c} for s, c in post_status_facet],
            "post_column": [{"name": n, "count": c} for n, c in post_column_facet],
            "product_status": [{"status": s, "count": c} for s, c in product_status_facet],
        }
    })
