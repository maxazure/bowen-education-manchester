# -*- coding: utf-8 -*-
"""全局异常处理器

处理所有未捕获的异常，返回友好的错误页面
"""

import logging

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings

logger = logging.getLogger("docms")
templates = Jinja2Templates(directory=str(settings.template_dir))


async def http_exception_handler(request: Request, exc: HTTPException) -> HTMLResponse:
    """
    处理 HTTP 异常 (404, 403, etc.)

    Args:
        request: FastAPI Request 对象
        exc: HTTPException 异常

    Returns:
        HTMLResponse 错误页面
    """
    logger.warning(
        f"HTTP {exc.status_code}: {exc.detail} - "
        f"URL: {request.url.path} - "
        f"IP: {request.client.host if request.client else 'unknown'}"
    )

    # 404 错误 - 页面不存在
    if exc.status_code == 404:
        try:
            return templates.TemplateResponse(
                "404.html",
                {"request": request, "path": request.url.path},
                status_code=404,
            )
        except Exception as e:
            logger.error(f"Failed to render 404.html: {e}")
            # 如果模板不存在，返回简单的HTML
            return HTMLResponse(
                content=f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>404 - Page Not Found</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                        h1 {{ color: #333; }}
                    </style>
                </head>
                <body>
                    <h1>404 - Page Not Found</h1>
                    <p>The page you requested could not be found.</p>
                    <a href="/">Return to Homepage</a>
                </body>
                </html>
                """,
                status_code=404,
            )

    # 其他 HTTP 错误
    try:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "status_code": exc.status_code, "detail": exc.detail},
            status_code=exc.status_code,
        )
    except Exception as e:
        logger.error(f"Failed to render error.html: {e}")
        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error {exc.status_code}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                    h1 {{ color: #d32f2f; }}
                </style>
            </head>
            <body>
                <h1>Error {exc.status_code}</h1>
                <p>{exc.detail}</p>
                <a href="/">Return to Homepage</a>
            </body>
            </html>
            """,
            status_code=exc.status_code,
        )


async def global_exception_handler(request: Request, exc: Exception) -> HTMLResponse:
    """
    处理所有未捕获的异常

    Args:
        request: FastAPI Request 对象
        exc: Exception 异常

    Returns:
        HTMLResponse 500 错误页面
    """
    logger.error(
        f"Unhandled exception: {type(exc).__name__}: {str(exc)} - "
        f"URL: {request.url.path} - "
        f"IP: {request.client.host if request.client else 'unknown'}",
        exc_info=True,  # 记录完整的堆栈跟踪
    )

    # 生产环境不显示详细错误信息
    error_message = str(exc) if settings.debug else "Internal Server Error"

    try:
        return templates.TemplateResponse(
            "500.html",
            {"request": request, "error": error_message, "debug": settings.debug},
            status_code=500,
        )
    except Exception as e:
        logger.error(f"Failed to render 500.html: {e}")
        # 如果模板不存在，返回简单的HTML
        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>500 - Internal Server Error</title>
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                    h1 {{ color: #d32f2f; }}
                    pre {{ text-align: left; background: #f5f5f5; padding: 15px; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <h1>500 - Internal Server Error</h1>
                <p>We're sorry, but something went wrong.</p>
                {'<pre>' + error_message + '</pre>' if settings.debug else ''}
                <p><a href="/">Return to Homepage</a></p>
            </body>
            </html>
            """,
            status_code=500,
        )
