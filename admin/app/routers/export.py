"""
数据导出路由
"""

import csv
import io
import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models import Post, Product, ContactMessage, Gallery, SiteColumn, ProductCategory

router = APIRouter(tags=["export"])


def escape_csv(value):
    """转义CSV特殊字符"""
    if value is None:
        return ''
    value = str(value)
    if '"' in value or ',' in value or '\n' in value:
        return f'"{value.replace("\"", "\"\"")}"'
    return value


@router.get("/export/posts")
async def export_posts(
    request: Request,
    format: str = Query("csv", enum=["csv", "json"]),
    column_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """导出文章数据"""
    from datetime import datetime as dt

    query = db.query(Post).options()

    if column_id:
        query = query.filter(Post.column_id == column_id)
    if status_filter:
        query = query.filter(Post.status == status_filter)
    if start_date:
        try:
            start = dt.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Post.created_at >= start)
        except:
            pass
    if end_date:
        try:
            end = dt.strptime(end_date, '%Y-%m-%d')
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(Post.created_at <= end)
        except:
            pass

    posts = query.order_by(Post.created_at.desc()).all()

    if format == "json":
        data = [{
            "id": p.id,
            "title": p.title,
            "title_en": p.title_en,
            "slug": p.slug,
            "summary": p.summary,
            "column_id": p.column_id,
            "status": p.status,
            "is_recommended": p.is_recommended,
            "is_pinned": p.is_pinned,
            "view_count": p.view_count,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "updated_at": p.updated_at.isoformat() if p.updated_at else None,
            "published_at": p.published_at.isoformat() if p.published_at else None,
        } for p in posts]

        return JSONResponse(content={
            "success": True,
            "data": data,
            "exported_at": datetime.now().isoformat(),
            "total": len(data)
        })

    # CSV format
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'ID', '标题', '英文标题', 'Slug', '摘要', '栏目ID', '状态',
        '推荐', '置顶', '浏览量', '创建时间', '更新时间', '发布时间'
    ])

    # Write data
    for p in posts:
        writer.writerow([
            p.id,
            escape_csv(p.title),
            escape_csv(p.title_en),
            escape_csv(p.slug),
            escape_csv(p.summary),
            p.column_id,
            p.status,
            '是' if p.is_recommended else '否',
            '是' if p.is_pinned else '否',
            p.view_count or 0,
            p.created_at.strftime('%Y-%m-%d %H:%M:%S') if p.created_at else '',
            p.updated_at.strftime('%Y-%m-%d %H:%M:%S') if p.updated_at else '',
            p.published_at.strftime('%Y-%m-%d %H:%M:%S') if p.published_at else '',
        ])

    filename = f"posts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/products")
async def export_products(
    request: Request,
    format: str = Query("csv", enum=["csv", "json"]),
    category_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """导出产品数据"""
    query = db.query(Product)

    if category_id:
        query = query.filter(Product.category_id == category_id)
    if status:
        query = query.filter(Product.status == status)

    products = query.order_by(Product.created_at.desc()).all()

    if format == "json":
        data = [{
            "id": p.id,
            "name": p.name,
            "name_en": p.name_en,
            "slug": p.slug,
            "description": p.description,
            "price": p.price,
            "category_id": p.category_id,
            "status": p.status,
            "is_featured": p.is_featured,
            "view_count": p.view_count,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        } for p in products]

        return JSONResponse(content={
            "success": True,
            "data": data,
            "exported_at": datetime.now().isoformat(),
            "total": len(data)
        })

    # CSV format
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'ID', '名称', '英文名称', 'Slug', '描述', '价格', '栏目ID',
        '状态', '推荐', '浏览量', '创建时间'
    ])

    for p in products:
        writer.writerow([
            p.id,
            escape_csv(p.name),
            escape_csv(p.name_en),
            escape_csv(p.slug),
            escape_csv(p.description),
            p.price or 0,
            p.category_id,
            p.status,
            '是' if p.is_featured else '否',
            p.view_count or 0,
            p.created_at.strftime('%Y-%m-%d %H:%M:%S') if p.created_at else '',
        ])

    filename = f"products_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/contacts")
async def export_contacts(
    request: Request,
    format: str = Query("csv", enum=["csv", "json"]),
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """导出留言数据"""
    from datetime import datetime as dt

    query = db.query(ContactMessage)

    if status:
        query = query.filter(ContactMessage.status == status)
    if start_date:
        try:
            start = dt.strptime(start_date, '%Y-%m-%d')
            query = query.filter(ContactMessage.created_at >= start)
        except:
            pass
    if end_date:
        try:
            end = dt.strptime(end_date, '%Y-%m-%d')
            end = end.replace(hour=23, minute=59, second=59)
            query = query.filter(ContactMessage.created_at <= end)
        except:
            pass

    contacts = query.order_by(ContactMessage.created_at.desc()).all()

    if format == "json":
        data = [{
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "subject": c.subject,
            "message": c.message,
            "status": c.status,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        } for c in contacts]

        return JSONResponse(content={
            "success": True,
            "data": data,
            "exported_at": datetime.now().isoformat(),
            "total": len(data)
        })

    # CSV format
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'ID', '姓名', '邮箱', '电话', '主题', '留言内容', '状态', '创建时间'
    ])

    for c in contacts:
        writer.writerow([
            c.id,
            escape_csv(c.name),
            escape_csv(c.email),
            escape_csv(c.phone),
            escape_csv(c.subject),
            escape_csv(c.message),
            c.status,
            c.created_at.strftime('%Y-%m-%d %H:%M:%S') if c.created_at else '',
        ])

    filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/galleries")
async def export_galleries(
    request: Request,
    format: str = Query("csv", enum=["csv", "json"]),
    db: Session = Depends(get_db),
):
    """导出相册数据"""
    galleries = db.query(Gallery).order_by(Gallery.created_at.desc()).all()

    if format == "json":
        data = [{
            "id": g.id,
            "title": g.title,
            "title_en": g.title_en,
            "description": g.description,
            "image_count": len(g.images) if g.images else 0,
            "status": g.status,
            "created_at": g.created_at.isoformat() if g.created_at else None,
        } for g in galleries]

        return JSONResponse(content={
            "success": True,
            "data": data,
            "exported_at": datetime.now().isoformat(),
            "total": len(data)
        })

    # CSV format
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        'ID', '标题', '英文标题', '描述', '图片数量', '状态', '创建时间'
    ])

    for g in galleries:
        writer.writerow([
            g.id,
            escape_csv(g.title),
            escape_csv(g.title_en),
            escape_csv(g.description),
            len(g.images) if g.images else 0,
            g.status,
            g.created_at.strftime('%Y-%m-%d %H:%M:%S') if g.created_at else '',
        ])

    filename = f"galleries_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/stats")
async def export_all_stats(
    request: Request,
    db: Session = Depends(get_db),
):
    """导出完整统计报告"""
    from sqlalchemy import func

    # 文章统计
    posts_count = db.query(func.count(Post.id)).scalar()
    posts_published = db.query(func.count(Post.id)).filter(Post.status == 'published').scalar()
    posts_draft = db.query(func.count(Post.id)).filter(Post.status == 'draft').scalar()

    # 产品统计
    products_count = db.query(func.count(Product.id)).scalar()
    products_active = db.query(func.count(Product.id)).filter(Product.status == 'active').scalar()

    # 留言统计
    contacts_count = db.query(func.count(ContactMessage.id)).scalar()
    contacts_unread = db.query(func.count(ContactMessage.id)).filter(ContactMessage.status == 'unread').scalar()

    # 相册统计
    galleries_count = db.query(func.count(Gallery.id)).scalar()

    report = {
        "report_time": datetime.now().isoformat(),
        "posts": {
            "total": posts_count,
            "published": posts_published,
            "draft": posts_draft,
        },
        "products": {
            "total": products_count,
            "active": products_active,
        },
        "contacts": {
            "total": contacts_count,
            "unread": contacts_unread,
        },
        "galleries": {
            "total": galleries_count,
        }
    }

    return JSONResponse(content={
        "success": True,
        "data": report
    })
