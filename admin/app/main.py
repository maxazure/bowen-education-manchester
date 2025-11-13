"""
管理后台应用入口

独立的FastAPI应用，可以单独运行。
"""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# 使用相对导入避免命名冲突
from .routers import auth, media, columns, single_pages, posts, products, settings, galleries, contacts
from .middleware import AdminAuthMiddleware

# 获取admin目录的绝对路径
ADMIN_DIR = Path(__file__).parent.parent

# 创建FastAPI应用
app = FastAPI(
    title="博文教育管理后台",
    description="Bowen Education Admin System",
    version="1.0.0",
)

# 添加Session中间件（必须在认证中间件之前）
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
)

# 添加认证中间件
app.add_middleware(AdminAuthMiddleware)

# 注册路由
app.include_router(auth.router, prefix="/admin", tags=["auth"])
app.include_router(media.router, prefix="/admin/media", tags=["media"])
app.include_router(columns.router, prefix="/admin", tags=["columns"])
app.include_router(single_pages.router, prefix="/admin", tags=["pages"])
app.include_router(posts.router, prefix="/admin", tags=["posts"])
app.include_router(products.router, prefix="/admin", tags=["products"])
app.include_router(settings.router, prefix="/admin", tags=["settings"])
app.include_router(galleries.router, prefix="/admin", tags=["galleries"])
app.include_router(contacts.router, prefix="/admin", tags=["contacts"])

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(ADMIN_DIR / "static")), name="static")

# 配置模板
templates = Jinja2Templates(directory=str(ADMIN_DIR / "templates"))


from fastapi import Request
from fastapi.responses import HTMLResponse


@app.get("/")
async def root():
    """根路径"""
    return {"message": "博文教育管理后台API", "version": "1.0.0"}


@app.get("/admin/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """管理后台仪表板"""
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
