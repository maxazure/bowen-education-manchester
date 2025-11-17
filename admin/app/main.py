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
from .routers import auth, media, columns, single_pages, posts, products, settings, galleries, contacts, home, column_builder, static_pages
from .middleware import AdminAuthMiddleware

# 获取admin目录的绝对路径
ADMIN_DIR = Path(__file__).parent.parent
# 获取项目根目录
PROJECT_ROOT = ADMIN_DIR.parent

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
    session_cookie="admin_session",
    max_age=14400,  # 4小时
    same_site="lax",
    https_only=False,  # 开发环境使用HTTP
)

# 添加认证中间件
app.add_middleware(AdminAuthMiddleware)

# 注册路由（移除 /admin 前缀，因为挂载时会自动添加）
app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(media.router, prefix="/media", tags=["media"])
app.include_router(columns.router, prefix="", tags=["columns"])
app.include_router(single_pages.router, prefix="", tags=["pages"])
app.include_router(posts.router, prefix="", tags=["posts"])
app.include_router(products.router, prefix="", tags=["products"])
app.include_router(settings.router, prefix="", tags=["settings"])
app.include_router(galleries.router, prefix="", tags=["galleries"])
app.include_router(contacts.router, prefix="", tags=["contacts"])
app.include_router(home.router, prefix="", tags=["home"])
app.include_router(column_builder.router, prefix="", tags=["columns-builder"])
app.include_router(static_pages.router, prefix="", tags=["static-pages"])

# 挂载管理后台静态文件
app.mount("/admin-static", StaticFiles(directory=str(ADMIN_DIR / "admin-static")), name="admin-static")

# 挂载静态文件（使用前台的 templates/static 目录）
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "templates" / "static")), name="static")

# 配置模板
templates = Jinja2Templates(directory=str(ADMIN_DIR / "templates"))


from fastapi import Request
from fastapi.responses import HTMLResponse


@app.get("/")
async def root():
    """根路径"""
    return {"message": "博文教育管理后台API", "version": "1.0.0"}


@app.get("/", response_class=HTMLResponse)
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
