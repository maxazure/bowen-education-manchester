"""
管理后台应用入口

独立的FastAPI应用，可以单独运行。
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# 加载环境变量
load_dotenv()

# 使用相对导入避免命名冲突
from .routers import auth, media, columns, single_pages, posts, products, settings, galleries, contacts, home, column_builder, static_pages, heroes, stats, notifications, export, export_page, comments, import_, import_page, search, backup, trash, operation_logs, reports, i18n, advanced_search, users, roles, health, dashboard, versions, sitemap, seo, scheduler, tags, analytics, export_data
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

# 添加认证中间件（BaseHTTPMiddleware）
# 注意：SessionMiddleware 必须在最后添加，这样它才会在最外层执行
app.add_middleware(AdminAuthMiddleware)

# 添加Session中间件（最后添加，在最外层执行）
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv(
        "SECRET_KEY",
        "dev-secret-key-for-testing-only-32chars"
    ),
    session_cookie="admin_session",
    max_age=int(os.getenv("ADMIN_SESSION_TIMEOUT", "14400")),  # 4小时
    same_site="lax",  # lax 适合本地开发和跨站请求
    https_only=False,  # 本地开发使用 HTTP
)

# 注册路由
# auth 路由保持在根路径（/login, /logout）
app.include_router(auth.router, prefix="", tags=["auth"])
# 其他管理后台路由添加 /admin 前缀
app.include_router(media.router, prefix="/admin/media", tags=["media"])
app.include_router(columns.router, prefix="/admin/columns", tags=["columns"])
app.include_router(single_pages.router, prefix="/admin/pages", tags=["pages"])
app.include_router(posts.router, prefix="/admin/posts", tags=["posts"])
app.include_router(products.router, prefix="/admin/products", tags=["products"])
app.include_router(settings.router, prefix="/admin/settings", tags=["settings"])
app.include_router(galleries.router, prefix="/admin/galleries", tags=["galleries"])
app.include_router(heroes.router, prefix="/admin/heroes", tags=["heroes"])
app.include_router(contacts.router, prefix="/admin/contacts", tags=["contacts"])
app.include_router(home.router, prefix="/admin/home", tags=["home"])
app.include_router(column_builder.router, prefix="/admin/columns", tags=["columns-builder"])
app.include_router(static_pages.router, prefix="/admin/static-pages", tags=["static-pages"])
app.include_router(stats.router, prefix="/admin/stats", tags=["stats"])
app.include_router(notifications.router, prefix="/admin", tags=["notifications"])
app.include_router(export.router, prefix="/admin", tags=["export"])
app.include_router(export_page.router, prefix="/admin", tags=["export-page"])
app.include_router(comments.router, prefix="/admin", tags=["comments"])
app.include_router(import_.router, prefix="/admin", tags=["import"])
app.include_router(import_page.router, prefix="/admin", tags=["import-page"])
app.include_router(search.router, prefix="/admin", tags=["search"])
app.include_router(backup.router, prefix="/admin", tags=["backup"])
app.include_router(trash.router, prefix="/admin", tags=["trash"])
app.include_router(operation_logs.router, prefix="/admin", tags=["operation-log"])
app.include_router(reports.router, prefix="/admin", tags=["reports"])
app.include_router(i18n.router, prefix="/admin", tags=["i18n"])
app.include_router(advanced_search.router, prefix="/admin", tags=["advanced-search"])
app.include_router(users.router, prefix="/admin", tags=["users"])
app.include_router(roles.router, prefix="/admin", tags=["roles"])
app.include_router(health.router, prefix="/admin", tags=["health"])
app.include_router(dashboard.router, prefix="/admin", tags=["dashboard"])
app.include_router(versions.router, prefix="/admin", tags=["versions"])
app.include_router(sitemap.router, prefix="/admin", tags=["sitemap"])
app.include_router(seo.router, prefix="/admin", tags=["seo"])
app.include_router(scheduler.router, prefix="/admin", tags=["scheduler"])
app.include_router(tags.router, prefix="/admin", tags=["tags"])
app.include_router(analytics.router, prefix="/admin", tags=["analytics"])
app.include_router(export_data.router, prefix="/admin", tags=["export"])

# 挂载管理后台静态文件
app.mount("/admin-static", StaticFiles(directory=str(ADMIN_DIR / "admin-static")), name="admin-static")

# 挂载静态文件（使用前台的 templates/static 目录）
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "templates" / "static")), name="static")

# 配置模板
templates = Jinja2Templates(directory=str(ADMIN_DIR / "templates"))


from fastapi import Request
from fastapi.responses import HTMLResponse


@app.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """管理后台仪表板"""
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard_alias(request: Request):
    """管理后台仪表板（/admin 别名）"""
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
