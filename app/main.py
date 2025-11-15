# -*- coding: utf-8 -*-
"""FastAPI Application Factory and Entry Point

Docms CMS - Browns Bay Language School Website
"""

import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import APP_ENV, SiteConfig, settings
from app.middleware.error_handlers import (
    global_exception_handler,
    http_exception_handler,
)
from app.routes import frontend, health
from app.utils.logger import setup_logging

logger = logging.getLogger("docms")


def create_app(
    site_config: Optional[SiteConfig] = None,
    template_dir: Optional[Path] = None,
    static_dir: Optional[Path] = None,
    database_url: Optional[str] = None,
) -> FastAPI:
    """
    创建 FastAPI 应用实例

    Args:
        site_config: 站点配置对象
        template_dir: 模板目录路径
        static_dir: 静态文件目录路径
        database_url: 数据库 URL

    Returns:
        配置好的 FastAPI 应用实例
    """
    # 使用默认配置或传入的配置
    if site_config is None:
        site_config = SiteConfig()

    # 创建 FastAPI 应用
    app = FastAPI(
        title=site_config.site_name,
        description=site_config.site_description,
        version="1.0.0",
    )

    # 存储配置到 app.state
    app.state.config = site_config
    app.state.template_dir = template_dir or site_config.template_dir
    app.state.static_dir = static_dir or site_config.static_dir
    app.state.database_url = database_url or site_config.database_url

    # 配置日志
    setup_logging("docms", log_level=site_config.log_level.lower())
    logger.info(f"{site_config.site_name} 启动成功")
    logger.info(f"模板目录: {app.state.template_dir}")
    logger.info(f"数据库: {app.state.database_url}")

    # 注册中间件（必须在路由之前）
    register_middlewares(app)

    # 注册路由（包括管理后台）
    register_routes(app)

    # 挂载静态文件
    if app.state.static_dir.exists():
        app.mount(
            "/static",
            StaticFiles(directory=str(app.state.static_dir)),
            name="static"
        )

    # 挂载管理后台静态文件
    from pathlib import Path
    admin_static_dir = Path(__file__).parent.parent / "admin" / "admin-static"
    if admin_static_dir.exists():
        app.mount(
            "/admin-static",
            StaticFiles(directory=str(admin_static_dir)),
            name="admin-static"
        )

    # 注册异常处理
    register_exception_handlers(app)

    # 启动事件
    @app.on_event("startup")
    async def startup_event():
        logger.info(f"{site_config.site_name} 启动成功")
        logger.info(f"模板目录: {app.state.template_dir}")
        logger.info(f"数据库: {app.state.database_url}")

    return app


def register_middlewares(app: FastAPI):
    """注册所有中间件（必须在路由之前调用）"""
    from admin.app.middleware import AdminAuthMiddleware
    from starlette.middleware.sessions import SessionMiddleware
    import os

    # 添加管理后台认证中间件
    # 注意：中间件注册顺序很重要，后注册的先执行
    # 所以 AdminAuthMiddleware 要先注册，这样 SessionMiddleware 会先执行
    app.add_middleware(AdminAuthMiddleware)

    # 添加 Session 中间件（管理后台需要）
    # SessionMiddleware 后注册，所以会先执行，确保 session 可用
    app.add_middleware(
        SessionMiddleware,
        secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-in-production"),
        session_cookie="admin_session",
        max_age=14400,  # 4小时
        same_site="lax",
        https_only=False,
    )


def register_routes(app: FastAPI):
    """注册所有路由"""
    # 先注册管理后台路由（在通配符路由之前）
    from admin.app.routers import auth, media, columns, single_pages, posts, products, settings, galleries, contacts, dashboard, home, column_builder

    # 注册管理后台路由
    app.include_router(auth.router, prefix="/admin", tags=["admin-auth"])
    app.include_router(dashboard.router, prefix="/admin", tags=["admin-dashboard"])
    app.include_router(media.router, prefix="/admin/media", tags=["admin-media"])
    app.include_router(columns.router, prefix="/admin", tags=["admin-columns"])
    app.include_router(single_pages.router, prefix="/admin", tags=["admin-pages"])
    app.include_router(posts.router, prefix="/admin", tags=["admin-posts"])
    app.include_router(products.router, prefix="/admin", tags=["admin-products"])
    app.include_router(settings.router, prefix="/admin", tags=["admin-settings"])
    app.include_router(galleries.router, prefix="/admin", tags=["admin-galleries"])
    app.include_router(contacts.router, prefix="/admin", tags=["admin-contacts"])
    app.include_router(home.router, prefix="/admin", tags=["admin-home"])
    app.include_router(column_builder.router, prefix="/admin", tags=["admin-columns-builder"])

    # 注册前台路由
    app.include_router(health.router, tags=["health"])
    app.include_router(frontend.router, tags=["frontend"])


def register_exception_handlers(app: FastAPI):
    """注册异常处理器"""
    from fastapi.exceptions import HTTPException

    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: HTTPException):
        """404 错误处理"""
        try:
            templates = Jinja2Templates(directory=str(app.state.template_dir))
            return templates.TemplateResponse(
                "404.html",
                {"request": request},
                status_code=404
            )
        except Exception:
            return HTMLResponse(
                content="<h1>404 - Page Not Found</h1>",
                status_code=404
            )

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: Exception):
        """500 错误处理"""
        logger.error(f"Internal error: {exc}")
        try:
            templates = Jinja2Templates(directory=str(app.state.template_dir))
            return templates.TemplateResponse(
                "500.html",
                {"request": request},
                status_code=500
            )
        except Exception:
            return HTMLResponse(
                content="<h1>500 - Internal Server Error</h1>",
                status_code=500
            )


# 创建默认应用实例（用于直接运行）
logger = setup_logging("docms", log_level="DEBUG" if settings.debug else "INFO")
logger.info(f"Starting {settings.app_name} in {APP_ENV} mode")

app = create_app()
logger.info("Application routes registered")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
