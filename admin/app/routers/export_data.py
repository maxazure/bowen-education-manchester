"""数据导出路由"""

import csv
import io
import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import Post, Product, ContactMessage, MediaFile

router = APIRouter(tags=["export"])


def format_csv_data(data: list, headers: list) -> str:
    """格式化 CSV 数据"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)

    for item in data:
        row = []
        for header in headers:
            key = header.lower().replace(' ', '_')
            value = item.get(key, '')
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, bool):
                value = '是' if value else '否'
            row.append(str(value) if value else '')
        writer.writerow(row)

    return output.getvalue()


@router.get("/api/export/{content_type}")
async def export_data(
    content_type: str,
    format: str = Query("csv", regex="^(csv|json|excel)$"),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """导出数据 API"""
    try:
        if content_type == "posts":
            return await export_posts(db, format, date_from, date_to)
        elif content_type == "products":
            return await export_products(db, format, date_from, date_to)
        elif content_type == "contacts":
            return await export_contacts(db, format, date_from, date_to)
        elif content_type == "media":
            return await export_media_stats(db, format)
        elif content_type == "analytics":
            return await export_analytics(db, format, date_from, date_to)
        else:
            return JSONResponse(
                content={"success": False, "message": "不支持的导出类型"},
                status_code=400
            )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"导出失败: {str(e)}"},
            status_code=500
        )


async def export_posts(db: Session, format: str, date_from: str, date_to: str):
    """导出文章数据"""
    query = db.query(Post)

    if date_from:
        query = query.filter(Post.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(Post.created_at <= datetime.strptime(date_to + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))

    posts = query.all()

    data = []
    for post in posts:
        data.append({
            "ID": post.id,
            "标题": post.title,
            "状态": post.status,
            "栏目": post.column.name if post.column else '',
            "作者": post.author or '',
            "创建时间": post.created_at,
            "更新时间": post.updated_at,
            "浏览次数": post.view_count or 0,
            "SEO标题": post.seo_title or '',
            "SEO描述": post.seo_description or '',
        })

    if format == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2, default=str)
        return StreamingResponse(
            io.StringIO(content),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=posts_export_{datetime.now().strftime('%Y%m%d')}.json"}
        )
    else:
        csv_content = format_csv_data(data, ["ID", "标题", "状态", "栏目", "作者", "创建时间", "更新时间", "浏览次数", "SEO标题", "SEO描述"])
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename=posts_export_{datetime.now().strftime('%Y%m%d')}.csv"}
        )


async def export_products(db: Session, format: str, date_from: str, date_to: str):
    """导出产品数据"""
    query = db.query(Product)

    if date_from:
        query = query.filter(Product.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(Product.created_at <= datetime.strptime(date_to + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))

    products = query.all()

    data = []
    for product in products:
        data.append({
            "ID": product.id,
            "名称": product.name,
            "价格": product.price,
            "分类": product.category.name if product.category else '',
            "状态": product.status,
            "库存": product.stock or 0,
            "创建时间": product.created_at,
        })

    if format == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2, default=str)
        return StreamingResponse(
            io.StringIO(content),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=products_export_{datetime.now().strftime('%Y%m%d')}.json"}
        )
    else:
        csv_content = format_csv_data(data, ["ID", "名称", "价格", "分类", "状态", "库存", "创建时间"])
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename=products_export_{datetime.now().strftime('%Y%m%d')}.csv"}
        )


async def export_contacts(db: Session, format: str, date_from: str, date_to: str):
    """导出留言数据"""
    query = db.query(ContactMessage)

    if date_from:
        query = query.filter(ContactMessage.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(ContactMessage.created_at <= datetime.strptime(date_to + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))

    contacts = query.order_by(ContactMessage.created_at.desc()).all()

    data = []
    for contact in contacts:
        data.append({
            "ID": contact.id,
            "姓名": contact.name,
            "邮箱": contact.email,
            "电话": contact.phone or '',
            "主题": contact.subject,
            "状态": contact.status,
            "创建时间": contact.created_at,
        })

    if format == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2, default=str)
        return StreamingResponse(
            io.StringIO(content),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=contacts_export_{datetime.now().strftime('%Y%m%d')}.json"}
        )
    else:
        csv_content = format_csv_data(data, ["ID", "姓名", "邮箱", "电话", "主题", "状态", "创建时间"])
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename=contacts_export_{datetime.now().strftime('%Y%m%d')}.csv"}
        )


async def export_media_stats(db: Session, format: str):
    """导出媒体库统计"""
    total_files = db.query(MediaFile).count()
    total_images = db.query(MediaFile).filter(MediaFile.file_type == 'image').count()
    total_videos = db.query(MediaFile).filter(MediaFile.file_type == 'video').count()
    total_docs = db.query(MediaFile).filter(MediaFile.file_type == 'document').count()

    data = {
        "导出时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "总文件数": total_files,
        "图片数": total_images,
        "视频数": total_videos,
        "文档数": total_docs,
    }

    if format == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2)
        return StreamingResponse(
            io.StringIO(content),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=media_stats_{datetime.now().strftime('%Y%m%d')}.json"}
        )
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["指标", "数值"])
        for key, value in data.items():
            writer.writerow([key, value])
        return StreamingResponse(
            io.StringIO(output.getvalue()),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename=media_stats_{datetime.now().strftime('%Y%m%d')}.csv"}
        )


async def export_analytics(db: Session, format: str, date_from: str, date_to: str):
    """导出访问统计"""
    from app.models import PageVisit

    query = db.query(PageVisit).order_by(PageVisit.visit_count.desc())

    if date_from:
        query = query.filter(PageVisit.last_visited_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(PageVisit.last_visited_at <= datetime.strptime(date_to + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))

    pages = query.limit(100).all()

    data = []
    for page in pages:
        data.append({
            "页面路径": page.page_path,
            "页面标题": page.page_title or '',
            "访问次数": page.visit_count,
            "最后访问": page.last_visited_at,
    })

    if format == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2, default=str)
        return StreamingResponse(
            io.StringIO(content),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=analytics_export_{datetime.now().strftime('%Y%m%d')}.json"}
        )
    else:
        csv_content = format_csv_data(data, ["页面路径", "页面标题", "访问次数", "最后访问"])
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename=analytics_export_{datetime.now().strftime('%Y%m%d')}.csv"}
        )
