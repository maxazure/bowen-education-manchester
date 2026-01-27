"""
角色管理数据库初始化

创建默认角色和设置初始权限
"""

import json
from app.database import SessionLocal
from app.models.admin_user import Role, UserRole, PERMISSIONS

def get_default_roles():
    """获取默认角色配置"""
    return [
        {
            "name": "超级管理员",
            "code": UserRole.SUPER_ADMIN.value,
            "description": "拥有所有权限，可以管理系统所有功能",
            "is_system": True,
            "permissions": ["*"],  # * 表示所有权限
        },
        {
            "name": "管理员",
            "code": UserRole.ADMIN.value,
            "description": "拥有大部分管理权限，不能修改系统设置和用户",
            "is_system": True,
            "permissions": [
                "post:create", "post:read", "post:update", "post:delete", "post:publish",
                "product:create", "product:read", "product:update", "product:delete",
                "media:upload", "media:read", "media:delete",
                "gallery:create", "gallery:read", "gallery:update", "gallery:delete",
                "system:backup", "system:logs",
            ],
        },
        {
            "name": "编辑",
            "code": UserRole.EDITOR.value,
            "description": "可以创建和编辑内容，但不能删除或发布",
            "is_system": True,
            "permissions": [
                "post:create", "post:read", "post:update",
                "product:create", "product:read", "product:update",
                "media:upload", "media:read",
                "gallery:create", "gallery:read", "gallery:update",
            ],
        },
        {
            "name": "投稿人",
            "code": UserRole.CONTRIBUTOR.value,
            "description": "可以创建内容但不能发布",
            "is_system": True,
            "permissions": [
                "post:create", "post:read",
                "product:create", "product:read",
                "media:upload", "media:read",
                "gallery:create", "gallery:read",
            ],
        },
        {
            "name": "查看者",
            "code": UserRole.VIEWER.value,
            "description": "只能查看内容，不能创建或修改",
            "is_system": True,
            "permissions": [
                "post:read",
                "product:read",
                "media:read",
                "gallery:read",
            ],
        },
    ]


def init_roles():
    """初始化角色数据"""
    db = SessionLocal()
    try:
        # 检查是否已有角色
        existing_roles = db.query(Role).count()
        if existing_roles > 0:
            print(f"角色已存在 ({existing_roles}个)，跳过初始化")
            return

        # 创建默认角色
        default_roles = get_default_roles()
        for role_data in default_roles:
            role = Role(
                name=role_data["name"],
                code=role_data["code"],
                description=role_data["description"],
                is_system=role_data["is_system"],
            )
            role.set_permissions(role_data["permissions"])
            db.add(role)
            print(f"创建角色: {role_data['name']}")

        db.commit()
        print("角色初始化完成!")
    finally:
        db.close()


def update_existing_admin_role():
    """为现有管理员用户分配超级管理员角色"""
    db = SessionLocal()
    try:
        from app.models import AdminUser

        # 查找超级管理员角色
        super_admin_role = db.query(Role).filter(
            Role.code == UserRole.SUPER_ADMIN.value
        ).first()

        if not super_admin_role:
            print("超级管理员角色不存在，请先运行 init_roles")
            return

        # 查找第一个用户并分配角色
        first_user = db.query(AdminUser).first()
        if first_user:
            first_user.role_id = super_admin_role.id
            db.commit()
            print(f"已将用户 {first_user.username} 设为超级管理员")
        else:
            print("没有找到用户")
    finally:
        db.close()


if __name__ == "__main__":
    print("初始化角色数据...")
    init_roles()
    print("\n更新现有用户角色...")
    update_existing_admin_role()
