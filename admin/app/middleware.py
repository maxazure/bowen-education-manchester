"""
管理后台中间件
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse


class AdminAuthMiddleware(BaseHTTPMiddleware):
    """
    管理后台认证中间件

    检查用户是否已登录，未登录则重定向到登录页。
    """

    async def dispatch(self, request: Request, call_next):
        # TODO: 在用户管理模块中实现
        # 公开路径（无需认证）
        public_paths = ["/login", "/health", "/static"]

        # 检查是否是公开路径
        is_public = any(request.url.path.startswith(path) for path in public_paths)

        if not is_public:
            # 检查session中是否有用户信息
            user_id = request.session.get("admin_user_id")
            if not user_id:
                # 未登录，重定向到登录页
                return RedirectResponse(url="/login", status_code=302)

        response = await call_next(request)
        return response
