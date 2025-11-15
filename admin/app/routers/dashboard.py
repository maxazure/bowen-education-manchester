"""
管理后台仪表板路由
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="admin/templates")


@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """
    管理后台仪表板

    Args:
        request: FastAPI request 对象

    Returns:
        仪表板页面 HTML
    """
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )
