"""
管理后台中间件
"""
import os
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

logger = logging.getLogger(__name__)


class AdminAuthMiddleware(BaseHTTPMiddleware):
    """
    管理后台认证中间件

    检查用户是否已登录，未登录则重定向到登录页。
    """

    async def dispatch(self, request: Request, call_next):
        # 测试环境跳过认证
        if os.getenv("TESTING") == "1":
            response = await call_next(request)
            return response

        # 公开路径（无需认证）- 前缀匹配
        public_prefixes = ["/admin/login", "/admin/logout", "/admin/api/", "/admin/static/", "/api/"]
        static_paths = ["/static/", "/admin-static/", "/uploads/", "/health"]

        # 检查是否是静态资源或公开路径
        for static_path in static_paths:
            if request.url.path.startswith(static_path):
                response = await call_next(request)
                return response

        # 如果是管理后台路径且不是公开路径
        if request.url.path.startswith("/admin"):
            # 检查是否是公开路径（前缀匹配）
            if any(request.url.path.startswith(p) for p in public_prefixes):
                pass  # 公开路径，继续处理
            else:
                # 需要认证的管理后台路径
                try:
                    # 先检查 session 是否存在
                    if hasattr(request, 'session'):
                        user_id = request.session.get("admin_user_id")
                        logger.info(f"访问 {request.url.path}, session user_id: {user_id}, session内容: {dict(request.session)}")
                    else:
                        logger.error("request.session 属性不存在")
                        user_id = None
                except (AttributeError, RuntimeError, AssertionError) as e:
                    logger.error(f"Session读取异常: {e}")
                    user_id = None

                if not user_id:
                    logger.warning(f"未登录用户访问: {request.url.path}")
                    if request.method == "GET":
                        return RedirectResponse(url="/admin/login", status_code=302)
                    else:
                        from fastapi.responses import JSONResponse
                        return JSONResponse({"detail": "未授权"}, status_code=401)

        response = await call_next(request)
        return response
