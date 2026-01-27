"""
导入页面路由
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models import SiteColumn, ProductCategory

router = APIRouter(tags=["import-page"])


@router.get("/import", response_class=HTMLResponse)
async def import_page(
    request: Request,
    db: Session = Depends(get_db),
):
    """数据导入页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 获取栏目列表
    columns = db.query(SiteColumn).order_by(SiteColumn.sort_order).all()

    # 获取产品分类
    categories = db.query(ProductCategory).order_by(ProductCategory.sort_order).all()

    return templates.TemplateResponse("import.html", {
        "request": request,
        "columns": columns,
        "categories": categories,
    })
