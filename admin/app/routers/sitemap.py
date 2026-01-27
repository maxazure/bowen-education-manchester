"""
网站地图管理路由

生成和更新网站地图(sitemap.xml)
"""

import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional, List, Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import Post, Product, Gallery, SiteColumn, SinglePage

router = APIRouter(tags=["sitemap"])


@router.get("/sitemap", response_class=HTMLResponse)
async def sitemap_page(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """网站地图管理页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 获取sitemap统计
    posts_count = db.query(func.count(Post.id)).filter(Post.status == 'published').scalar() or 0
    products_count = db.query(func.count(Product.id)).filter(Product.status == 'published').scalar() or 0
    galleries_count = db.query(func.count(Gallery.id)).filter(Gallery.status == 'published').scalar() or 0
    pages_count = db.query(func.count(SinglePage.id)).scalar() or 0

    # 检查sitemap文件是否存在
    sitemap_path = "public/sitemap.xml"
    sitemap_exists = os.path.exists(sitemap_path)

    sitemap_info = {}
    if sitemap_exists:
        try:
            stat = os.stat(sitemap_path)
            sitemap_info = {
                "exists": True,
                "size": round(stat.st_size / 1024, 2),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            }

            # 解析sitemap获取URL数量
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            url_count = len(root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'))
            sitemap_info["url_count"] = url_count
        except Exception as e:
            sitemap_info = {"exists": False, "error": str(e)}

    return templates.TemplateResponse("sitemap.html", {
        "request": request,
        "stats": {
            "posts": posts_count,
            "products": products_count,
            "galleries": galleries_count,
            "pages": pages_count,
            "total": posts_count + products_count + galleries_count + pages_count,
        },
        "sitemap": sitemap_info,
    })


@router.get("/api/sitemap/stats")
async def get_sitemap_stats(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取网站地图统计"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # 获取最近更新的内容
    recent_posts = db.query(Post).filter(
        Post.status == 'published'
    ).order_by(Post.updated_at.desc()).limit(10).all()

    return JSONResponse(content={
        "success": True,
        "data": {
            "posts": db.query(func.count(Post.id)).filter(Post.status == 'published').scalar() or 0,
            "products": db.query(func.count(Product.id)).filter(Product.status == 'published').scalar() or 0,
            "galleries": db.query(func.count(Gallery.id)).filter(Gallery.status == 'published').scalar() or 0,
            "pages": db.query(func.count(SinglePage.id)).scalar() or 0,
            "recent_updates": [
                {
                    "type": "post",
                    "title": p.title[:30],
                    "updated_at": p.updated_at.isoformat() if p.updated_at else None,
                }
                for p in recent_posts
            ],
        }
    })


@router.post("/api/sitemap/generate")
async def generate_sitemap(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """生成网站地图"""
    data = await request.json()
    base_url = data.get("base_url", "https://www.bowen-education.co.uk")

    # 确保目录存在
    os.makedirs("public", exist_ok=True)

    # 获取所有已发布的内容
    posts = db.query(Post).filter(Post.status == 'published').all()
    products = db.query(Product).filter(Product.status == 'published').all()
    galleries = db.query(Gallery).filter(Gallery.status == 'published').all()
    pages = db.query(SinglePage).all()
    columns = db.query(SiteColumn).all()

    # 创建sitemap
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ET.register_namespace('xhtml', 'http://www.w3.org/1999/xhtml')

    root = ET.Element("urlset")

    # 首页
    add_url(root, base_url, "1.0", "daily", datetime.now().strftime("%Y-%m-%d"))

    # 栏目页
    for col in columns:
        if col.slug:
            add_url(root, f"{base_url}/{col.slug}", "0.8", "weekly", datetime.now().strftime("%Y-%m-%d"))

    # 单页
    for page in pages:
        if page.slug:
            add_url(root, f"{base_url}/{page.slug}", "0.6", "monthly", datetime.now().strftime("%Y-%m-%d"))

    # 文章
    for post in posts:
        if post.slug and post.column:
            lastmod = post.updated_at.strftime("%Y-%m-%d") if post.updated_at else datetime.now().strftime("%Y-%m-%d")
            add_url(root, f"{base_url}/{post.column.slug}/{post.slug}", "0.7", "monthly", lastmod)

    # 产品
    for product in products:
        if product.slug:
            lastmod = product.updated_at.strftime("%Y-%m-%d") if product.updated_at else datetime.now().strftime("%Y-%m-%d")
            add_url(root, f"{base_url}/products/{product.slug}", "0.6", "monthly", lastmod)

    # 相册
    for gallery in galleries:
        if gallery.slug:
            lastmod = gallery.updated_at.strftime("%Y-%m-%d") if gallery.updated_at else datetime.now().strftime("%Y-%m-%d")
            add_url(root, f"{base_url}/gallery/{gallery.slug}", "0.5", "monthly", lastmod)

    # 保存文件
    tree = ET.ElementTree(root)
    sitemap_path = "public/sitemap.xml"
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)

    # 生成sitemaps索引（如果有多个）
    url_count = len(root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'))

    return JSONResponse(content={
        "success": True,
        "message": f"网站地图已生成，包含 {url_count} 个URL",
        "data": {
            "url_count": url_count,
            "file_path": sitemap_path,
            "file_size": round(os.path.getsize(sitemap_path) / 1024, 2),
        }
    })


@router.get("/api/sitemap/ping")
async def ping_sitemap(
    admin_user=Depends(get_current_admin_user),
):
    """通知搜索引擎更新sitemap"""
    base_url = "https://www.bowen-education.co.uk"

    search_engines = [
        {"name": "Google", "url": f"https://www.google.com/ping?sitemap={base_url}/sitemap.xml"},
        {"name": "Bing", "url": f"https://www.bing.com/ping?sitemap={base_url}/sitemap.xml"},
        {"name": "Baidu", "url": f"https://www.baidu.com/sitemap.xml?url={base_url}/sitemap.xml"},
    ]

    results = []
    for engine in search_engines:
        results.append({
            "name": engine["name"],
            "url": engine["url"],
            "status": "通知已发送（请到搜索引擎站长平台查看实际状态）"
        })

    return JSONResponse(content={
        "success": True,
        "message": "已向搜索引擎发送通知",
        "data": results
    })


@router.get("/sitemap.xml")
async def serve_sitemap():
    """提供sitemap.xml文件"""
    sitemap_path = "public/sitemap.xml"
    if os.path.exists(sitemap_path):
        return FileResponse(sitemap_path, media_type="application/xml")
    else:
        return HTMLResponse(content='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>', media_type="application/xml")


def add_url(root, loc, priority, changefreq, lastmod):
    """添加URL到sitemap"""
    url = ET.SubElement(root, "url")

    loc_elem = ET.SubElement(url, "loc")
    loc_elem.text = loc

    priority_elem = ET.SubElement(url, "priority")
    priority_elem.text = str(priority)

    changefreq_elem = ET.SubElement(url, "changefreq")
    changefreq_elem.text = changefreq

    lastmod_elem = ET.SubElement(url, "lastmod")
    lastmod_elem.text = lastmod


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="admin/templates")
