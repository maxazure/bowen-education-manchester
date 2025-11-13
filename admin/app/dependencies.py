"""
管理后台依赖注入
"""


from fastapi import Depends, Request
from sqlalchemy.orm import Session

from .database import get_db


async def get_current_admin_user(request: Request):
    """
    获取当前登录的管理员

    TODO: 在用户管理模块中实现
    """
    return None


async def require_admin(request: Request, db: Session = Depends(get_db)):
    """
    要求用户必须是管理员

    TODO: 在用户管理模块中实现
    """
    pass
