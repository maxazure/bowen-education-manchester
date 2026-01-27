"""
用户管理路由

管理员用户管理和权限控制
"""

import json
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import or_, and_, func, desc
from sqlalchemy.orm import Session, joinedload

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import AdminUser, Role, UserRole, PERMISSIONS

router = APIRouter(tags=["users"])


def check_permission(admin_user: AdminUser, permission: str) -> bool:
    """检查用户是否有特定权限"""
    return admin_user.has_permission(permission)


@router.get("/users", response_class=HTMLResponse)
async def users_page(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """用户管理页面"""
    if not check_permission(admin_user, "user:read"):
        raise HTTPException(status_code=403, detail="没有查看用户的权限")

    templates = Jinja2Templates(directory="admin/templates")

    # 获取所有用户
    users = db.query(AdminUser).options(joinedload(AdminUser.role)).order_by(
        desc(AdminUser.created_at)
    ).all()

    # 获取所有角色
    roles = db.query(Role).all()

    # 统计信息
    stats = {
        "total_users": db.query(func.count(AdminUser.id)).scalar(),
        "active_users": db.query(func.count(AdminUser.id)).filter(
            AdminUser.is_active == True
        ).scalar(),
        "total_roles": db.query(func.count(Role.id)).scalar(),
    }

    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users,
        "roles": roles,
        "stats": stats,
        "permissions": PERMISSIONS,
    })


@router.get("/api/users")
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str = Query(""),
    role_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取用户列表API"""
    if not check_permission(admin_user, "user:read"):
        return JSONResponse(
            content={"success": False, "message": "没有查看用户的权限"},
            status_code=403
        )

    query = db.query(AdminUser).options(joinedload(AdminUser.role))

    # 搜索
    if keyword:
        query = query.filter(
            or_(
                AdminUser.username.contains(keyword),
                AdminUser.email.contains(keyword),
                AdminUser.display_name.contains(keyword),
            )
        )

    # 筛选角色
    if role_id:
        query = query.filter(AdminUser.role_id == role_id)

    # 筛选状态
    if is_active is not None:
        query = query.filter(AdminUser.is_active == is_active)

    # 统计总数
    total = query.count()

    # 分页
    users = query.order_by(desc(AdminUser.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return JSONResponse(content={
        "success": True,
        "data": {
            "items": [
                {
                    "id": u.id,
                    "username": u.username,
                    "email": u.email,
                    "display_name": u.display_name or u.username,
                    "avatar": u.avatar,
                    "is_active": u.is_active,
                    "role_id": u.role_id,
                    "role_name": u.role.name if u.role else "无角色",
                    "role_code": u.role.code if u.role else None,
                    "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None,
                    "login_count": u.login_count,
                    "created_at": u.created_at.isoformat() if u.created_at else None,
                }
                for u in users
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    })


@router.get("/api/users/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取单个用户信息"""
    if not check_permission(admin_user, "user:read"):
        return JSONResponse(
            content={"success": False, "message": "没有查看用户的权限"},
            status_code=403
        )

    user = db.query(AdminUser).options(joinedload(AdminUser.role)).filter(
        AdminUser.id == user_id
    ).first()

    if not user:
        return JSONResponse(
            content={"success": False, "message": "用户不存在"},
            status_code=404
        )

    return JSONResponse(content={
        "success": True,
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "display_name": user.display_name,
            "avatar": user.avatar,
            "is_active": user.is_active,
            "role_id": user.role_id,
            "role_name": user.role.name if user.role else "无角色",
            "permissions": user.role.get_permissions_list() if user.role else [],
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
            "login_count": user.login_count,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
    })


@router.post("/api/users")
async def create_user(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """创建新用户"""
    if not check_permission(admin_user, "user:create"):
        return JSONResponse(
            content={"success": False, "message": "没有创建用户的权限"},
            status_code=403
        )

    data = await request.json()

    # 验证必填字段
    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if not data.get(field):
            return JSONResponse(
                content={"success": False, "message": f"缺少必填字段: {field}"},
                status_code=400
            )

    # 检查用户名和邮箱是否已存在
    existing = db.query(AdminUser).filter(
        or_(
            AdminUser.username == data["username"],
            AdminUser.email == data["email"],
        )
    ).first()
    if existing:
        return JSONResponse(
            content={"success": False, "message": "用户名或邮箱已存在"},
            status_code=400
        )

    # 创建用户
    user = AdminUser(
        username=data["username"],
        email=data["email"],
        display_name=data.get("display_name") or data["username"],
    )
    user.set_password(data["password"])

    # 设置角色
    if data.get("role_id"):
        role = db.query(Role).filter(Role.id == data["role_id"]).first()
        if role:
            user.role_id = role.id

    db.add(user)
    db.commit()
    db.refresh(user)

    # 记录操作日志
    log_content = f"创建用户: {user.username}"
    log_params = {
        "action": "create_user",
        "user_id": user.id,
        "username": user.username,
    }

    return JSONResponse(content={
        "success": True,
        "message": "用户创建成功",
        "data": {"id": user.id},
    })


@router.put("/api/users/{user_id}")
async def update_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """更新用户信息"""
    if not check_permission(admin_user, "user:update"):
        return JSONResponse(
            content={"success": False, "message": "没有编辑用户的权限"},
            status_code=403
        )

    user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
    if not user:
        return JSONResponse(
            content={"success": False, "message": "用户不存在"},
            status_code=404
        )

    # 不能修改超级管理员（除非自己是超级管理员）
    if user.role and user.role.code == UserRole.SUPER_ADMIN.value:
        if not (admin_user.role and admin_user.role.code == UserRole.SUPER_ADMIN.value):
            return JSONResponse(
                content={"success": False, "message": "不能修改超级管理员"},
                status_code=403
            )

    data = await request.json()

    # 更新字段
    if data.get("email") and data["email"] != user.email:
        # 检查邮箱是否已被使用
        existing = db.query(AdminUser).filter(
            and_(
                AdminUser.email == data["email"],
                AdminUser.id != user_id,
            )
        ).first()
        if existing:
            return JSONResponse(
                content={"success": False, "message": "邮箱已被使用"},
                status_code=400
            )
        user.email = data["email"]

    if "display_name" in data:
        user.display_name = data["display_name"]

    if "avatar" in data:
        user.avatar = data["avatar"]

    if "is_active" in data:
        user.is_active = data["is_active"]

    # 只有超级管理员可以修改角色
    if data.get("role_id") is not None:
        if admin_user.role and admin_user.role.code == UserRole.SUPER_ADMIN.value:
            user.role_id = data["role_id"]
        else:
            return JSONResponse(
                content={"success": False, "message": "只有超级管理员可以修改用户角色"},
                status_code=403
            )

    # 只有自己可以修改密码，或者超级管理员可以修改他人密码
    if data.get("password"):
        if user.id == admin_user.id or (
            admin_user.role and admin_user.role.code == UserRole.SUPER_ADMIN.value
        ):
            user.set_password(data["password"])
        else:
            return JSONResponse(
                content={"success": False, "message": "只能修改自己的密码"},
                status_code=403
            )

    db.commit()
    db.refresh(user)

    return JSONResponse(content={
        "success": True,
        "message": "用户更新成功",
    })


@router.delete("/api/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """删除用户"""
    if not check_permission(admin_user, "user:delete"):
        return JSONResponse(
            content={"success": False, "message": "没有删除用户的权限"},
            status_code=403
        )

    user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
    if not user:
        return JSONResponse(
            content={"success": False, "message": "用户不存在"},
            status_code=404
        )

    # 不能删除自己
    if user.id == admin_user.id:
        return JSONResponse(
            content={"success": False, "message": "不能删除自己"},
            status_code=400
        )

    # 不能删除超级管理员
    if user.role and user.role.code == UserRole.SUPER_ADMIN.value:
        return JSONResponse(
            content={"success": False, "message": "不能删除超级管理员"},
            status_code=403
        )

    username = user.username
    db.delete(user)
    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": f"用户 {username} 已删除",
    })


@router.post("/api/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """激活用户"""
    if not check_permission(admin_user, "user:update"):
        return JSONResponse(
            content={"success": False, "message": "没有编辑用户的权限"},
            status_code=403
        )

    user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
    if not user:
        return JSONResponse(
            content={"success": False, "message": "用户不存在"},
            status_code=404
        )

    user.is_active = True
    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": f"用户 {user.username} 已激活",
    })


@router.post("/api/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """禁用用户"""
    if not check_permission(admin_user, "user:update"):
        return JSONResponse(
            content={"success": False, "message": "没有编辑用户的权限"},
            status_code=403
        )

    user = db.query(AdminUser).filter(AdminUser.id == user_id).first()
    if not user:
        return JSONResponse(
            content={"success": False, "message": "用户不存在"},
            status_code=404
        )

    # 不能禁用自己
    if user.id == admin_user.id:
        return JSONResponse(
            content={"success": False, "message": "不能禁用自己"},
            status_code=400
        )

    # 不能禁用超级管理员
    if user.role and user.role.code == UserRole.SUPER_ADMIN.value:
        return JSONResponse(
            content={"success": False, "message": "不能禁用超级管理员"},
            status_code=403
        )

    user.is_active = False
    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": f"用户 {user.username} 已禁用",
    })


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="admin/templates")
