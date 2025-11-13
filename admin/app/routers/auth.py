"""
管理后台认证路由

实现登录、登出和密码修改功能
"""

from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.admin_user import AdminUser

router = APIRouter()
templates = Jinja2Templates(directory="admin/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    登录页面

    Args:
        request: FastAPI request 对象

    Returns:
        登录页面 HTML
    """
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    登录处理

    Args:
        request: FastAPI request 对象
        username: 用户名
        password: 密码
        db: 数据库会话

    Returns:
        成功则重定向到仪表板，失败则返回登录页面with error
    """
    # 查询管理员
    admin = db.query(AdminUser).filter(AdminUser.username == username).first()

    # 验证用户名和密码
    if not admin or not admin.verify_password(password):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "用户名或密码错误"}
        )

    # 更新最后登录时间
    admin.last_login_at = datetime.now()
    db.commit()

    # 设置 Session
    request.session["admin_user_id"] = admin.id
    request.session["admin_username"] = admin.username

    # 重定向到仪表板
    return RedirectResponse(url="/admin/", status_code=302)


@router.get("/logout")
async def logout(request: Request):
    """
    登出

    Args:
        request: FastAPI request 对象

    Returns:
        重定向到登录页
    """
    # 清除 Session
    try:
        request.session.clear()
    except (AttributeError, RuntimeError, AssertionError):
        # 在测试环境中 session 可能未正确初始化
        pass

    # 重定向到登录页
    return RedirectResponse(url="/admin/login", status_code=302)


@router.get("/profile/change-password", response_class=HTMLResponse)
async def change_password_page(request: Request):
    """
    密码修改页面

    Args:
        request: FastAPI request 对象

    Returns:
        密码修改页面 HTML
    """
    return templates.TemplateResponse(
        "profile/change-password.html", {"request": request}
    )


@router.post("/profile/change-password")
async def change_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    密码修改处理

    Args:
        request: FastAPI request 对象
        old_password: 旧密码
        new_password: 新密码
        confirm_password: 确认新密码
        db: 数据库会话

    Returns:
        成功则重定向到仪表板，失败则返回密码修改页面with error
    """
    # 获取当前用户
    try:
        admin_user_id = request.session.get("admin_user_id")
    except (AttributeError, RuntimeError, AssertionError):
        # 在测试环境中 session 可能未正确初始化
        admin_user_id = None

    if not admin_user_id:
        return RedirectResponse(url="/admin/login", status_code=302)

    admin = db.query(AdminUser).filter(AdminUser.id == admin_user_id).first()

    # 验证旧密码
    if not admin.verify_password(old_password):
        return templates.TemplateResponse(
            "profile/change-password.html", {"request": request, "error": "旧密码错误"}
        )

    # 验证新密码一致性
    if new_password != confirm_password:
        return templates.TemplateResponse(
            "profile/change-password.html",
            {"request": request, "error": "两次输入的新密码不一致"},
        )

    # 更新密码
    admin.set_password(new_password)
    db.commit()

    # 重定向到仪表板
    return RedirectResponse(url="/admin/", status_code=302)
