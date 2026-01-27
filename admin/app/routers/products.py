"""
产品管理路由
"""

import math
import re
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from admin.app.database import get_db
from app.models.product import Product, ProductCategory
from app.models.site import ColumnType, SiteColumn
from app.services.product_service import can_delete_product, generate_slug
from app.services.single_page_service import html_to_markdown, markdown_to_html
from admin.app.routers.static_pages import generate_static_task

router = APIRouter(tags=["products"])

templates = Jinja2Templates(directory="admin/templates")


@router.get("", response_class=HTMLResponse)
async def list_products(
    request: Request,
    db: Session = Depends(get_db),
    column_id: Optional[int] = None,
    category: Optional[str] = None,
    status_filter: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
):
    """
    产品列表页

    支持筛选: column_id, category, status, keyword, page
    """
    # 基础查询
    query = db.query(Product).options(
        joinedload(Product.column),
        joinedload(Product.categories),
    )

    # 计算统计数字（用于模板显示）
    all_products = query.all()
    online_count = len([p for p in all_products if p.status == 'online'])
    offline_count = len([p for p in all_products if p.status == 'offline'])
    recommended_count = len([p for p in all_products if p.is_recommended])

    # 筛选条件
    if column_id:
        query = query.filter(Product.column_id == column_id)

    if category:
        query = query.join(Product.categories).filter(ProductCategory.slug == category)

    if status_filter:
        query = query.filter(Product.status == status_filter)

    if keyword:
        query = query.filter(
            (Product.name.contains(keyword)) | (Product.summary.contains(keyword))
        )

    # 排序: 推荐产品优先,然后按更新时间
    query = query.order_by(Product.is_recommended.desc(), Product.updated_at.desc())

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
    products = query.limit(page_size).offset(offset).all()

    # 获取所有栏目（类型为 PRODUCT）
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.column_type == ColumnType.PRODUCT)
        .order_by(SiteColumn.sort_order)
        .all()
    )

    # 获取所有分类
    categories = db.query(ProductCategory).order_by(ProductCategory.sort_order).all()

    return templates.TemplateResponse(
        "products/list.html",
        {
            "request": request,
            "products": products,
            "columns": columns,
            "categories": categories,
            "current_column_id": column_id,
            "current_category": category,
            "current_status": status_filter,
            "current_keyword": keyword,
            "page": page,
            "total_pages": total_pages,
            "total": total,
            "online_count": online_count,
            "offline_count": offline_count,
            "recommended_count": recommended_count,
        },
    )


@router.get("/new", response_class=HTMLResponse)
async def new_product_form(
    request: Request,
    db: Session = Depends(get_db),
):
    """新建产品表单"""
    # 获取所有栏目（类型为 PRODUCT）
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.column_type == ColumnType.PRODUCT)
        .order_by(SiteColumn.sort_order)
        .all()
    )

    # 获取所有分类
    categories = db.query(ProductCategory).order_by(ProductCategory.sort_order).all()

    return templates.TemplateResponse(
        "products/form.html",
        {
            "request": request,
            "product": None,
            "columns": columns,
            "categories": categories,
            "action": "/admin/products/create",
            "method": "POST",
        },
    )


@router.post("/create", response_class=JSONResponse)
async def create_product(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    column_id: int = Form(...),
    name: str = Form(...),
    slug: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    description_markdown: Optional[str] = Form(None),
    cover_media_id: Optional[int] = Form(None),
    price_text: Optional[str] = Form(None),
    availability_status: str = Form("in_stock"),
    category_ids: str = Form(""),  # 逗号分隔的分类 ID
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    # 英文字段
    name_en: Optional[str] = Form(None),
    summary_en: Optional[str] = Form(None),
    description_markdown_en: Optional[str] = Form(None),
    price_text_en: Optional[str] = Form(None),
    seo_title_en: Optional[str] = Form(None),
    seo_description_en: Optional[str] = Form(None),
    # 其他字段
    is_recommended: bool = Form(False),
    product_status: str = Form("draft"),
):
    """创建产品"""
    try:
        # 生成或验证 slug
        if not slug:
            slug = generate_slug(name, db)
        else:
            # 验证 slug 是否已存在
            existing_slug = slug
            counter = 1
            while True:
                existing = db.query(Product).filter(Product.slug == existing_slug).first()
                if not existing:
                    slug = existing_slug
                    break
                existing_slug = f"{slug}-{counter}"
                counter += 1

        # 转换中文 Markdown 为 HTML
        description_html = ""
        if description_markdown:
            description_html = markdown_to_html(description_markdown)

        # 转换英文 Markdown 为 HTML
        description_html_en = ""
        if description_markdown_en:
            description_html_en = markdown_to_html(description_markdown_en)

        # 创建产品
        product = Product(
            column_id=column_id,
            name=name,
            slug=slug,
            summary=summary,
            description_html=description_html,
            description_markdown=description_markdown or "",
            cover_media_id=cover_media_id,
            price_text=price_text,
            availability_status=availability_status,
            seo_title=seo_title,
            seo_description=seo_description,
            # 英文字段
            name_en=name_en,
            summary_en=summary_en,
            description_html_en=description_html_en,
            description_markdown_en=description_markdown_en or "",
            price_text_en=price_text_en,
            seo_title_en=seo_title_en,
            seo_description_en=seo_description_en,
            # 其他字段
            is_recommended=is_recommended,
            status=product_status,
        )

        db.add(product)
        db.flush()  # 获取 product.id

        # 设置分类
        if category_ids:
            cat_ids = [
                int(cid.strip()) for cid in category_ids.split(",") if cid.strip()
            ]
            categories = (
                db.query(ProductCategory).filter(ProductCategory.id.in_(cat_ids)).all()
            )
            product.categories = categories

        db.commit()
        db.refresh(product)

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": "产品创建成功",
                "product_id": product.id,
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"创建失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/{product_id}/edit", response_class=HTMLResponse)
async def edit_product_form(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db),
):
    """编辑产品表单"""
    product = (
        db.query(Product)
        .options(joinedload(Product.categories))
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")

    # 获取所有栏目（类型为 PRODUCT）
    columns = (
        db.query(SiteColumn)
        .filter(SiteColumn.column_type == ColumnType.PRODUCT)
        .order_by(SiteColumn.sort_order)
        .all()
    )

    # 获取所有分类
    categories = db.query(ProductCategory).order_by(ProductCategory.sort_order).all()

    # 准备markdown内容（优先使用保存的markdown，否则从HTML转换）
    description_markdown = product.description_markdown or html_to_markdown(product.description_html)

    # 如果英文markdown为空或HTML英文字段与中文字段相同（历史数据问题）
    # 从中文HTML中提取英文内容
    description_markdown_en = product.description_markdown_en
    if not description_markdown_en:
        # 先检查 description_html_en 是否为空或与 description_html 相同
        if not product.description_html_en or product.description_html_en == product.description_html:
            # 从混合内容中提取纯英文（去除中文）
            html_en_only = re.sub(r'[\u4e00-\u9fff]+', '', product.description_html)
            # 清理提取后的HTML（移除空标签和多余空白）
            html_en_only = re.sub(r'>\s*<', '><', html_en_only)  # 移除标签间空白
            html_en_only = re.sub(r'\s{2,}', ' ', html_en_only)  # 合并多余空白
            description_markdown_en = html_to_markdown(html_en_only)
        else:
            description_markdown_en = html_to_markdown(product.description_html_en)

    return templates.TemplateResponse(
        "products/form.html",
        {
            "request": request,
            "product": product,
            "description_markdown": description_markdown,
            "description_markdown_en": description_markdown_en,
            "columns": columns,
            "categories": categories,
            "action": f"/admin/products/{product_id}",
            "method": "POST",
        },
    )


@router.post("/{product_id}", response_class=JSONResponse)
async def update_product(
    request: Request,
    product_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    column_id: int = Form(...),
    name: str = Form(...),
    slug: Optional[str] = Form(None),
    summary: Optional[str] = Form(None),
    description_markdown: Optional[str] = Form(None),
    cover_media_id: Optional[int] = Form(None),
    price_text: Optional[str] = Form(None),
    availability_status: str = Form("in_stock"),
    category_ids: str = Form(""),
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    # 英文字段
    name_en: Optional[str] = Form(None),
    summary_en: Optional[str] = Form(None),
    description_markdown_en: Optional[str] = Form(None),
    price_text_en: Optional[str] = Form(None),
    seo_title_en: Optional[str] = Form(None),
    seo_description_en: Optional[str] = Form(None),
    # 其他字段
    is_recommended: bool = Form(False),
    product_status: str = Form("draft"),
):
    """更新产品"""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="产品不存在")

        # 生成或验证 slug
        if not slug:
            slug = generate_slug(name, db, exclude_id=product_id)

        # 转换中文 Markdown 为 HTML
        description_html = ""
        if description_markdown:
            description_html = markdown_to_html(description_markdown)

        # 转换英文 Markdown 为 HTML
        description_html_en = ""
        if description_markdown_en:
            description_html_en = markdown_to_html(description_markdown_en)

        # 更新中文字段
        product.column_id = column_id
        product.name = name
        product.slug = slug
        product.summary = summary
        product.description_html = description_html
        product.description_markdown = description_markdown or ""
        product.cover_media_id = cover_media_id
        product.price_text = price_text
        product.availability_status = availability_status
        product.seo_title = seo_title
        product.seo_description = seo_description

        # 更新英文字段
        product.name_en = name_en
        product.summary_en = summary_en
        product.description_html_en = description_html_en
        product.description_markdown_en = description_markdown_en or ""
        product.price_text_en = price_text_en
        product.seo_title_en = seo_title_en
        product.seo_description_en = seo_description_en

        # 更新其他字段
        product.is_recommended = is_recommended
        product.status = product_status

        # 更新分类
        if category_ids:
            cat_ids = [
                int(cid.strip()) for cid in category_ids.split(",") if cid.strip()
            ]
            categories = (
                db.query(ProductCategory).filter(ProductCategory.id.in_(cat_ids)).all()
            )
            product.categories = categories
        else:
            product.categories = []

        db.commit()
        db.refresh(product)

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": "产品更新成功",
                "product_id": product.id,
            },
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"更新失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.delete("/{product_id}", response_class=JSONResponse)
async def delete_product(
    product_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """删除产品"""
    try:
        # 检查是否可以删除
        can_delete, error_msg = can_delete_product(db, product_id)
        if not can_delete:
            return JSONResponse(
                content={"success": False, "message": error_msg},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="产品不存在")

        db.delete(product)
        db.commit()

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={"success": True, "message": "产品已移到回收站"},
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
async def list_trashed_products(
    request: Request,
    db: Session = Depends(get_db),
    page: int = 1,
):
    """回收站 - 已删除产品列表"""
    query = db.query(Product).options(
        joinedload(Product.column),
        joinedload(Product.categories),
    ).filter(Product.status == "trashed")

    query = query.order_by(Product.updated_at.desc())

    page_size = 20
    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    offset = (page - 1) * page_size
    products = query.limit(page_size).offset(offset).all()

    return templates.TemplateResponse(
        "products/trash.html",
        {
            "request": request,
            "products": products,
            "page": page,
            "total_pages": total_pages,
            "total": total,
        },
    )


@router.post("/trash/{product_id}/restore", response_class=JSONResponse)
async def restore_trashed_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """恢复已删除的产品"""
    try:
        product = db.query(Product).filter(Product.id == product_id, Product.status == "trashed").first()
        if not product:
            return JSONResponse(
                content={"success": False, "message": "产品不存在或未被删除"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        product.status = "draft"
        db.commit()

        return JSONResponse(
            content={"success": True, "message": "产品已恢复到草稿箱"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"恢复失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/trash/{product_id}/permanent-delete", response_class=JSONResponse)
async def permanent_delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """永久删除产品"""
    try:
        product = db.query(Product).filter(Product.id == product_id, Product.status == "trashed").first()
        if not product:
            return JSONResponse(
                content={"success": False, "message": "产品不存在或未被删除"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        product.categories = []
        db.delete(product)
        db.commit()

        return JSONResponse(
            content={"success": True, "message": "产品已永久删除"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/trash/empty", response_class=JSONResponse)
async def empty_product_trash(
    db: Session = Depends(get_db),
):
    """清空产品回收站"""
    try:
        trashed_products = db.query(Product).filter(Product.status == "trashed").all()

        count = 0
        for product in trashed_products:
            product.categories = []
            db.delete(product)
            count += 1

        db.commit()

        return JSONResponse(
            content={"success": True, "message": f"已永久删除 {count} 个产品"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"清空失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/check-slug", response_class=JSONResponse)
async def check_product_slug_unique(
    slug: str,
    exclude_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """检查 slug 是否唯一"""
    try:
        query = db.query(Product).filter(Product.slug == slug)
        if exclude_id:
            query = query.filter(Product.id != exclude_id)

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


@router.post("/duplicate/{product_id}", response_class=JSONResponse)
async def duplicate_product(
    product_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """复制产品"""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return JSONResponse(
                content={"success": False, "message": "产品不存在"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # 生成新的 slug
        new_slug = generate_slug(product.name + "-copy", db)

        # 创建新产品（复制所有字段）
        new_product = Product(
            column_id=product.column_id,
            name=product.name + " (副本)",
            slug=new_slug,
            summary=product.summary,
            description_markdown=product.description_markdown,
            description_html=product.description_html,
            cover_media_id=product.cover_media_id,
            price_text=product.price_text,
            availability_status=product.availability_status,
            seo_title=product.seo_title,
            seo_description=product.seo_description,
            name_en=product.name_en,
            summary_en=product.summary_en,
            description_markdown_en=product.description_markdown_en,
            description_html_en=product.description_html_en,
            price_text_en=product.price_text_en,
            seo_title_en=product.seo_title_en,
            seo_description_en=product.seo_description_en,
            is_recommended=False,  # 副本不继承推荐
            status="draft",  # 副本默认为草稿
        )

        db.add(new_product)
        db.flush()

        # 复制分类
        new_product.categories = product.categories

        db.commit()
        db.refresh(new_product)

        # 触发静态页面生成
        background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

        return JSONResponse(
            content={
                "success": True,
                "message": f"产品复制成功，新产品 ID: {new_product.id}",
                "new_product_id": new_product.id
            },
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"复制失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
