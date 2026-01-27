"""
数据导入路由
"""

import csv
import io
import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models import Post, Product, SiteColumn, ProductCategory

router = APIRouter(tags=["import"])


@router.get("/import", response_class=HTMLResponse)
async def import_page(
    request: Request,
):
    """数据导入页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    return templates.TemplateResponse("import.html", {
        "request": request,
    })


@router.post("/import/posts")
async def import_posts(
    request: Request,
    file: UploadFile = File(...),
    column_id: int = Form(...),
    db: Session = Depends(get_db),
):
    """导入文章数据"""
    try:
        # 读取文件内容
        content = await file.read()
        content = content.decode('utf-8-sig')

        # 解析 CSV
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)

        if not rows:
            return JSONResponse(
                content={"success": False, "message": "CSV 文件为空或格式不正确"},
                status_code=400
            )

        # 验证表头
        required_headers = ['title', 'content']
        headers = reader.fieldnames or []
        missing_headers = [h for h in required_headers if h not in headers]

        if missing_headers:
            return JSONResponse(
                content={"success": False, message=f"缺少必要的列: {', '.join(missing_headers)}"},
                status_code=400
            )

        # 获取栏目
        column = db.query(SiteColumn).filter(SiteColumn.id == column_id).first()
        if not column:
            return JSONResponse(
                content={"success": False, "message": "指定的栏目不存在"},
                status_code=400
            )

        # 导入数据
        imported = 0
        errors = []

        from app.services.post_service import generate_slug as post_generate_slug

        for idx, row in enumerate(rows, 1):
            try:
                title = row.get('title', '').strip()
                content = row.get('content', '').strip()
                summary = row.get('summary', '').strip() if row.get('summary') else None
                title_en = row.get('title_en', '').strip() if row.get('title_en') else None

                if not title or not content:
                    errors.append(f"第 {idx} 行: 标题和内容不能为空")
                    continue

                # 生成 slug
                slug = post_generate_slug(title, db)

                # 创建文章
                post = Post(
                    column_id=column_id,
                    title=title,
                    title_en=title_en,
                    slug=slug,
                    summary=summary,
                    content_html=content,
                    status='draft',
                )
                db.add(post)
                imported += 1

            except Exception as e:
                errors.append(f"第 {idx} 行: {str(e)}")

        db.commit()

        return JSONResponse(content={
            "success": True,
            "message": f"成功导入 {imported} 篇文章",
            "imported": imported,
            "errors": errors[:10] if len(errors) > 10 else errors,
            "total_errors": len(errors) if len(errors) > 10 else 0,
        })

    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"导入失败: {str(e)}"},
            status_code=500
        )


@router.post("/import/products")
async def import_products(
    request: Request,
    file: UploadFile = File(...),
    category_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    """导入产品数据"""
    try:
        content = await file.read()
        content = content.decode('utf-8-sig')

        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)

        if not rows:
            return JSONResponse(
                content={"success": False, "message": "CSV 文件为空或格式不正确"},
                status_code=400
            )

        required_headers = ['name', 'description']
        headers = reader.fieldnames or []
        missing_headers = [h for h in required_headers if h not in headers]

        if missing_headers:
            return JSONResponse(
                content={"success": False, message=f"缺少必要的列: {', '.join(missing_headers)}"},
                status_code=400
            )

        imported = 0
        errors = []

        for idx, row in enumerate(rows, 1):
            try:
                name = row.get('name', '').strip()
                description = row.get('description', '').strip()
                price = row.get('price', '').strip()
                name_en = row.get('name_en', '').strip() if row.get('name_en') else None

                if not name or not description:
                    errors.append(f"第 {idx} 行: 名称和描述不能为空")
                    continue

                # 生成 slug
                base_slug = name.lower().replace(' ', '-')
                slug = base_slug
                counter = 1
                while db.query(Product).filter(Product.slug == slug).first():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                # 解析价格
                try:
                    price_value = float(price) if price else 0
                except ValueError:
                    price_value = 0

                # 创建产品
                product = Product(
                    name=name,
                    name_en=name_en,
                    slug=slug,
                    description=description,
                    price=price_value,
                    category_id=category_id,
                    status='active',
                )
                db.add(product)
                imported += 1

            except Exception as e:
                errors.append(f"第 {idx} 行: {str(e)}")

        db.commit()

        return JSONResponse(content={
            "success": True,
            "message": f"成功导入 {imported} 个产品",
            "imported": imported,
            "errors": errors[:10] if len(errors) > 10 else errors,
            "total_errors": len(errors) if len(errors) > 10 else 0,
        })

    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"导入失败: {str(e)}"},
            status_code=500
        )


@router.get("/import/template/{type}")
async def download_template(
    type: str,
):
    """下载导入模板"""
    if type == "posts":
        headers = ['title', 'title_en', 'summary', 'content']
        filename = "posts_import_template.csv"
    elif type == "products":
        headers = ['name', 'name_en', 'description', 'price']
        filename = "products_import_template.csv"
    else:
        return JSONResponse(
            content={"success": False, "message": "不支持的模板类型"},
            status_code=400
        )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    # 添加示例数据
    if type == "posts":
        writer.writerow(['示例文章标题', 'Sample Article Title', '文章摘要...', '文章内容...'])
    else:
        writer.writerow(['示例产品名称', 'Sample Product Name', '产品描述...', '99.99'])

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv; charset=utf-8-sig",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
