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

        # 公开路径（无需认证）
        public_paths = ["/admin/login"]
        static_paths = ["/static/", "/admin-static/", "/uploads/", "/health"]

        # 检查是否是静态资源或公开路径
        for static_path in static_paths:
            if request.url.path.startswith(static_path):
                response = await call_next(request)
                return response

        # 如果是管理后台路径且不是公开路径
        if request.url.path.startswith("/admin") and request.url.path not in public_paths:
            # 检查 session 中是否有用户信息
            try:
                user_id = request.session.get("admin_user_id")
                logger.info(f"访问 {request.url.path}, session user_id: {user_id}, session内容: {dict(request.session)}")
            except (AttributeError, RuntimeError, AssertionError) as e:
                # 在测试环境中 session 可能未正确初始化
                logger.error(f"Session读取异常: {e}")
                user_id = None

            if not user_id:
                # 未登录，重定向到登录页
                logger.warning(f"未登录用户访问: {request.url.path}")
                if request.method == "GET":
                    return RedirectResponse(url="/admin/login", status_code=302)
                else:
                    # POST 请求返回 401
                    from fastapi.responses import JSONResponse

                    return JSONResponse({"detail": "未授权"}, status_code=401)

        response = await call_next(request)
        return response
