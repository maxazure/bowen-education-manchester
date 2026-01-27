"""
数据报表路由
"""

import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import Post, Product, Gallery, SiteColumn, SinglePage

router = APIRouter(tags=["reports"])


@router.get("/reports", response_class=HTMLResponse)
async def reports_page(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """数据报表页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    return templates.TemplateResponse("reports.html", {
        "request": request,
    })


@router.get("/api/reports/overview")
async def get_reports_overview(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取报表概览数据"""
    since = datetime.now() - timedelta(days=days)

    # 内容统计
    posts_count = db.query(func.count(Post.id)).scalar() or 0
    products_count = db.query(func.count(Product.id)).scalar() or 0
    galleries_count = db.query(func.count(Gallery.id)).scalar() or 0
    columns_count = db.query(func.count(SiteColumn.id)).scalar() or 0
    pages_count = db.query(func.count(SinglePage.id)).scalar() or 0

    # 文章状态统计
    published_posts = db.query(func.count(Post.id)).filter(Post.status == 'published').scalar() or 0
    draft_posts = db.query(func.count(Post.id)).filter(Post.status == 'draft').scalar() or 0
    offline_posts = db.query(func.count(Post.id)).filter(Post.status == 'offline').scalar() or 0

    # 特殊状态
    recommended_posts = db.query(func.count(Post.id)).filter(Post.is_recommended == True).scalar() or 0
    pinned_posts = db.query(func.count(Post.id)).filter(Post.is_pinned == True).scalar() or 0

    # 待审核
    pending_approval = db.query(func.count(Post.id)).filter(Post.is_approved == 0).scalar() or 0

    # 新增内容（指定周期内）
    new_posts = db.query(func.count(Post.id)).filter(Post.created_at >= since).scalar() or 0
    new_products = db.query(func.count(Product.id)).filter(Product.created_at >= since).scalar() or 0
    new_galleries = db.query(func.count(Gallery.id)).filter(Gallery.created_at >= since).scalar() or 0

    return JSONResponse(content={
        "success": True,
        "data": {
            "total": posts_count + products_count + galleries_count + columns_count + pages_count,
            "posts": posts_count,
            "products": products_count,
            "galleries": galleries_count,
            "columns": columns_count,
            "pages": pages_count,
            "publishedPosts": published_posts,
            "draftPosts": draft_posts,
            "offlinePosts": offline_posts,
            "recommendedPosts": recommended_posts,
            "pinnedPosts": pinned_posts,
            "pendingApproval": pending_approval,
            "monthlyPosts": new_posts,
            "monthlyProducts": new_products,
            "monthlyGalleries": new_galleries,
        }
    })


@router.get("/api/reports/trend")
async def get_trend_data(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取趋势数据"""
    since = datetime.now() - timedelta(days=days)

    # 按日期分组统计
    posts_by_date = (
        db.query(
            func.date(Post.created_at).label('date'),
            func.count(Post.id).label('count')
        )
        .filter(Post.created_at >= since)
        .group_by(func.date(Post.created_at))
        .order_by(func.date(Post.created_at))
        .all()
    )

    products_by_date = (
        db.query(
            func.date(Product.created_at).label('date'),
            func.count(Product.id).label('count')
        )
        .filter(Product.created_at >= since)
        .group_by(func.date(Product.created_at))
        .order_by(func.date(Product.created_at))
        .all()
    )

    galleries_by_date = (
        db.query(
            func.date(Gallery.created_at).label('date'),
            func.count(Gallery.id).label('count')
        )
        .filter(Gallery.created_at >= since)
        .group_by(func.date(Gallery.created_at))
        .order_by(func.date(Gallery.created_at))
        .all()
    )

    # 生成日期标签
    dates = []
    posts_data = []
    products_data = []
    galleries_data = []

    # 创建日期到数据的映射
    posts_map = {str(d.date): d.count for d in posts_by_date}
    products_map = {str(d.date): d.count for d in products_by_date}
    galleries_map = {str(d.date): d.count for d in galleries_by_date}

    current = since.date()
    end = datetime.now().date()

    while current <= end:
        date_str = str(current)
        dates.append(current.strftime('%m-%d'))
        posts_data.append(posts_map.get(date_str, 0))
        products_data.append(products_map.get(date_str, 0))
        galleries_data.append(galleries_map.get(date_str, 0))
        current += timedelta(days=1)

    return JSONResponse(content={
        "success": True,
        "data": {
            "labels": dates,
            "posts": posts_data,
            "products": products_data,
            "galleries": galleries_data,
        }
    })


@router.get("/api/reports/columns")
async def get_column_stats(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取栏目统计数据"""
    columns = db.query(SiteColumn).all()

    result = []
    for col in columns:
        posts_count = db.query(func.count(Post.id)).filter(Post.column_id == col.id).scalar() or 0

        # 统计该栏目的产品（通过栏目关联）
        products_count = 0
        if hasattr(col, 'products'):
            products_count = len(col.products) if col.products else 0

        # 统计该栏目的相册
        galleries_count = db.query(func.count(Gallery.id)).filter(Gallery.column_id == col.id).scalar() or 0

        result.append({
            "id": col.id,
            "name": col.name,
            "name_en": col.name_en,
            "posts": posts_count,
            "products": products_count,
            "galleries": galleries_count,
        })

    # 按内容总数排序
    result.sort(key=lambda x: x['posts'] + x['products'] + x['galleries'], reverse=True)

    return JSONResponse(content={
        "success": True,
        "data": result
    })


@router.get("/api/reports/summary")
async def get_summary_report(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取汇总报告（用于导出）"""
    since = datetime.now() - timedelta(days=days)

    # 基础统计
    stats = {
        "report_period": f"最近 {days} 天",
        "generated_at": datetime.now().isoformat(),
        "content_stats": {},
        "activity_stats": {},
    }

    # 内容统计
    stats["content_stats"]["posts"] = {
        "total": db.query(func.count(Post.id)).scalar() or 0,
        "published": db.query(func.count(Post.id)).filter(Post.status == 'published').scalar() or 0,
        "draft": db.query(func.count(Post.id)).filter(Post.status == 'draft').scalar() or 0,
        "offline": db.query(func.count(Post.id)).filter(Post.status == 'offline').scalar() or 0,
        "new": db.query(func.count(Post.id)).filter(Post.created_at >= since).scalar() or 0,
    }

    stats["content_stats"]["products"] = {
        "total": db.query(func.count(Product.id)).scalar() or 0,
        "active": db.query(func.count(Product.id)).filter(Product.status == 'active').scalar() or 0,
        "inactive": db.query(func.count(Product.id)).filter(Product.status == 'inactive').scalar() or 0,
    }

    stats["content_stats"]["galleries"] = {
        "total": db.query(func.count(Gallery.id)).scalar() or 0,
        "published": db.query(func.count(Gallery.id)).filter(Gallery.status == 'published').scalar() or 0,
        "draft": db.query(func.count(Gallery.id)).filter(Gallery.status == 'draft').scalar() or 0,
    }

    # 栏目统计
    columns = db.query(SiteColumn).all()
    stats["content_stats"]["columns"] = [
        {
            "name": col.name,
            "posts_count": db.query(func.count(Post.id)).filter(Post.column_id == col.id).scalar() or 0
        }
        for col in columns
    ]

    return JSONResponse(content={
        "success": True,
        "data": stats
    })


@router.get("/reports/export")
async def export_report(
    days: int = Query(30, ge=1, le=365),
    format: str = Query("json", regex="^(json|csv)$"),
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """导出报表"""
    from fastapi.responses import StreamingResponse
    import io

    since = datetime.now() - timedelta(days=days)

    # 获取数据
    posts = (
        db.query(Post)
        .filter(Post.created_at >= since)
        .order_by(desc(Post.created_at))
        .all()
    )

    # 生成CSV
    output = io.StringIO()
    output.write('\ufeff')  # BOM for Excel
    output.write("ID,标题,状态,栏目,创建时间,更新时间,是否推荐,是否置顶\n")

    for post in posts:
        status_map = {"published": "已发布", "draft": "草稿", "offline": "已下线"}
        output.write(
            f"{post.id},\"{post.title}\","
            f"{status_map.get(post.status, post.status)},"
            f"{post.column.name if post.column else ''},"
            f"{post.created_at.strftime('%Y-%m-%d %H:%M:%S')},"
            f"{post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else ''},"
            f"{'是' if post.is_recommended else '否'},"
            f"{'是' if post.is_pinned else '否'}\n"
        )

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=report_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )
