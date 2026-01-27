"""
角色管理路由

角色和权限管理
"""

import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import or_, func, desc
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import AdminUser, Role, UserRole, PERMISSIONS

router = APIRouter(tags=["roles"])


def check_permission(admin_user: AdminUser, permission: str) -> bool:
    """检查用户是否有特定权限"""
    return admin_user.has_permission(permission)


@router.get("/roles", response_class=HTMLResponse)
async def roles_page(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """角色管理页面"""
    if not check_permission(admin_user, "user:read"):
        raise HTTPException(status_code=403, detail="没有查看角色的权限")

    templates = Jinja2Templates(directory="admin/templates")

    # 获取所有角色
    roles = db.query(Role).order_by(Role.id).all()

    # 统计信息
    stats = {
        "total_roles": db.query(func.count(Role.id)).scalar(),
        "system_roles": db.query(func.count(Role.id)).filter(Role.is_system == True).scalar(),
        "custom_roles": db.query(func.count(Role.id)).filter(Role.is_system == False).scalar(),
    }

    return templates.TemplateResponse("roles.html", {
        "request": request,
        "roles": roles,
        "stats": stats,
        "permissions": PERMISSIONS,
        "user_roles": UserRole,
    })


@router.get("/api/roles")
async def get_roles(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取角色列表API"""
    if not check_permission(admin_user, "user:read"):
        return JSONResponse(
            content={"success": False, "message": "没有查看角色的权限"},
            status_code=403
        )

    roles = db.query(Role).order_by(Role.id).all()

    return JSONResponse(content={
        "success": True,
        "data": [
            {
                "id": r.id,
                "name": r.name,
                "code": r.code,
                "description": r.description,
                "is_system": r.is_system,
                "permissions": r.get_permissions_list(),
                "user_count": len(r.users),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in roles
        ]
    })


@router.get("/api/roles/{role_id}")
async def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取角色详情"""
    if not check_permission(admin_user, "user:read"):
        return JSONResponse(
            content={"success": False, "message": "没有查看角色的权限"},
            status_code=403
        )

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        return JSONResponse(
            content={"success": False, "message": "角色不存在"},
            status_code=404
        )

    return JSONResponse(content={
        "success": True,
        "data": {
            "id": role.id,
            "name": role.name,
            "code": role.code,
            "description": role.description,
            "is_system": role.is_system,
            "permissions": role.get_permissions_list(),
            "user_count": len(role.users),
            "created_at": role.created_at.isoformat() if role.created_at else None,
        }
    })


@router.post("/api/roles")
async def create_role(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """创建角色"""
    # 只有超级管理员可以创建角色
    if not (admin_user.role and admin_user.role.code == UserRole.SUPER_ADMIN.value):
        return JSONResponse(
            content={"success": False, "message": "只有超级管理员可以创建角色"},
            status_code=403
        )

    data = await request.json()

    # 验证必填字段
    if not data.get("name") or not data.get("code"):
        return JSONResponse(
            content={"success": False, "message": "角色名称和代码为必填项"},
            status_code=400
        )

    # 检查角色代码是否已存在
    existing = db.query(Role).filter(Role.code == data["code"]).first()
    if existing:
        return JSONResponse(
            content={"success": False, "message": "角色代码已存在"},
            status_code=400
        )

    # 创建角色
    role = Role(
        name=data["name"],
        code=data["code"],
        description=data.get("description"),
        is_system=False,
    )

    # 设置权限
    permissions = data.get("permissions", [])
    role.set_permissions(permissions)

    db.add(role)
    db.commit()
    db.refresh(role)

    return JSONResponse(content={
        "success": True,
        "message": "角色创建成功",
        "data": {"id": role.id},
    })


@router.put("/api/roles/{role_id}")
async def update_role(
    role_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """更新角色"""
    # 只有超级管理员可以修改角色
    if not (admin_user.role and admin_user.role.code == UserRole.SUPER_ADMIN.value):
        return JSONResponse(
            content={"success": False, "message": "只有超级管理员可以修改角色"},
            status_code=403
        )

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        return JSONResponse(
            content={"success": False, "message": "角色不存在"},
            status_code=404
        )

    # 不能修改系统内置角色
    if role.is_system:
        return JSONResponse(
            content={"success": False, "message": "不能修改系统内置角色"},
            status_code=403
        )

    data = await request.json()

    # 更新字段
    if data.get("name"):
        role.name = data["name"]

    if data.get("description") is not None:
        role.description = data["description"]

    # 更新权限
    if "permissions" in data:
        role.set_permissions(data["permissions"])

    db.commit()
    db.refresh(role)

    return JSONResponse(content={
        "success": True,
        "message": "角色更新成功",
    })


@router.delete("/api/roles/{role_id}")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """删除角色"""
    # 只有超级管理员可以删除角色
    if not (admin_user.role and admin_user.role.code == UserRole.SUPER_ADMIN.value):
        return JSONResponse(
            content={"success": False, "message": "只有超级管理员可以删除角色"},
            status_code=403
        )

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        return JSONResponse(
            content={"success": False, "message": "角色不存在"},
            status_code=404
        )

    # 不能删除系统内置角色
    if role.is_system:
        return JSONResponse(
            content={"success": False, "message": "不能删除系统内置角色"},
            status_code=403
        )

    # 检查是否有用户在使用此角色
    if role.users:
        return JSONResponse(
            content={"success": False, "message": f"该角色已被 {len(role.users)} 个用户使用，无法删除"},
            status_code=400
        )

    role_name = role.name
    db.delete(role)
    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": f"角色 {role_name} 已删除",
    })


@router.get("/api/permissions")
async def get_all_permissions(
    admin_user=Depends(get_current_admin_user),
):
    """获取所有权限定义"""
    # 将权限字典转换为列表格式
    permission_list = [
        {"key": key, "name": value}
        for key, value in PERMISSIONS.items()
    ]

    # 按模块分组
    modules = {}
    for perm in permission_list:
        module = perm["key"].split(":")[0]
        if module not in modules:
            modules[module] = {
                "name": {
                    "post": "文章",
                    "product": "产品",
                    "media": "媒体",
                    "gallery": "相册",
                    "user": "用户",
                    "system": "系统",
                }.get(module, module),
                "permissions": []
            }
        modules[module]["permissions"].append(perm)

    return JSONResponse(content={
        "success": True,
        "data": {
            "permissions": permission_list,
            "modules": modules,
        }
    })


@router.get("/api/my-permissions")
async def get_my_permissions(
    admin_user=Depends(get_current_admin_user),
):
    """获取当前用户的权限列表"""
    permissions = []
    for perm_key in PERMISSIONS.keys():
        if admin_user.has_permission(perm_key):
            permissions.append({
                "key": perm_key,
                "name": PERMISSIONS[perm_key],
            })

    return JSONResponse(content={
        "success": True,
        "data": {
            "role": admin_user.get_role_name(),
            "permissions": permissions,
            "is_super_admin": admin_user.role and admin_user.role.code == UserRole.SUPER_ADMIN.value,
        }
    })


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="admin/templates")
