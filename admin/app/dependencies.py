"""
管理后台依赖注入
"""


from fastapi import Depends, Request
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db


async def get_current_admin_user(request: Request):
    """
    获取当前登录的管理员

    从session中获取用户信息
    """
    user_id = request.session.get("admin_user_id")
    if not user_id:
        return None
    return {"id": user_id, "username": request.session.get("admin_username")}


async def require_admin(request: Request, db: Session = Depends(get_db)):
    """
    要求用户必须是管理员

    检查session中是否有有效的管理员登录信息
    """
    user_id = request.session.get("admin_user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录或登录已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 可以在这里添加数据库验证逻辑
    # 例如验证用户是否存在且为管理员

    return {"id": user_id, "username": request.session.get("admin_username")}


async def require_super_admin(request: Request, db: Session = Depends(get_db)):
    """
    要求用户必须是超级管理员

    检查session中是否有有效的管理员登录信息
    """
    user_id = request.session.get("admin_user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录或登录已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 可以在这里添加更严格的权限验证
    # 例如检查用户的角色是否为 super_admin

    return {"id": user_id, "username": request.session.get("admin_username")}
