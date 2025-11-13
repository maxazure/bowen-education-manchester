"""
产品管理路由
"""

import math
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.product import Product, ProductCategory
from app.models.site import ColumnType, SiteColumn
from app.services.product_service import can_delete_product, generate_slug
from app.services.single_page_service import markdown_to_html

router = APIRouter(prefix="/products", tags=["products"])

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
            "action": "/admin/products",
            "method": "POST",
        },
    )


@router.post("", response_class=JSONResponse)
async def create_product(
    request: Request,
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
    is_recommended: bool = Form(False),
    status: str = Form("draft"),
):
    """创建产品"""
    try:
        # 生成 slug
        if not slug:
            slug = generate_slug(name, db)

        # 转换 Markdown 为 HTML
        description_html = ""
        if description_markdown:
            description_html = markdown_to_html(description_markdown)

        # 创建产品
        product = Product(
            column_id=column_id,
            name=name,
            slug=slug,
            summary=summary,
            description_html=description_html,
            cover_media_id=cover_media_id,
            price_text=price_text,
            availability_status=availability_status,
            seo_title=seo_title,
            seo_description=seo_description,
            is_recommended=is_recommended,
            status=status,
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

    return templates.TemplateResponse(
        "products/form.html",
        {
            "request": request,
            "product": product,
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
    is_recommended: bool = Form(False),
    status: str = Form("draft"),
):
    """更新产品"""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="产品不存在")

        # 生成或验证 slug
        if not slug:
            slug = generate_slug(name, db, exclude_id=product_id)

        # 转换 Markdown 为 HTML
        description_html = ""
        if description_markdown:
            description_html = markdown_to_html(description_markdown)

        # 更新产品
        product.column_id = column_id
        product.name = name
        product.slug = slug
        product.summary = summary
        product.description_html = description_html
        product.cover_media_id = cover_media_id
        product.price_text = price_text
        product.availability_status = availability_status
        product.seo_title = seo_title
        product.seo_description = seo_description
        product.is_recommended = is_recommended
        product.status = status

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

        return JSONResponse(
            content={"success": True, "message": "产品删除成功"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
