"""
管理员用户模型

用于管理后台的管理员认证和授权
"""


import bcrypt
from enum import Enum as PyEnum
from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, PyEnum):
    """用户角色枚举"""
    SUPER_ADMIN = "super_admin"      # 超级管理员
    ADMIN = "admin"                  # 管理员
    EDITOR = "editor"                # 编辑
    CONTRIBUTOR = "contributor"      # 投稿人
    VIEWER = "viewer"                # 查看者


# 权限常量
PERMISSIONS = {
    # 文章权限
    "post:create": "创建文章",
    "post:read": "查看文章",
    "post:update": "编辑文章",
    "post:delete": "删除文章",
    "post:publish": "发布文章",

    # 产品权限
    "product:create": "创建产品",
    "product:read": "查看产品",
    "product:update": "编辑产品",
    "product:delete": "删除产品",

    # 媒体权限
    "media:upload": "上传媒体",
    "media:read": "查看媒体",
    "media:delete": "删除媒体",

    # 相册权限
    "gallery:create": "创建相册",
    "gallery:read": "查看相册",
    "gallery:update": "编辑相册",
    "gallery:delete": "删除相册",

    # 用户权限
    "user:create": "创建用户",
    "user:read": "查看用户",
    "user:update": "编辑用户",
    "user:delete": "删除用户",

    # 系统权限
    "system:settings": "系统设置",
    "system:backup": "数据备份",
    "system:logs": "查看日志",
}


class Role(Base):
    """角色表"""

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False)  # 系统内置角色，不可删除
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 权限列表（JSON格式）
    permissions = Column(Text, default="[]")

    # 关联用户
    users = relationship("AdminUser", back_populates="role")

    def get_permissions_list(self):
        """获取权限列表"""
        import json
        if self.permissions:
            return json.loads(self.permissions)
        return []

    def set_permissions(self, permissions_list):
        """设置权限列表"""
        import json
        self.permissions = json.dumps(permissions_list)

    def has_permission(self, permission):
        """检查是否有特定权限"""
        if self.code == UserRole.SUPER_ADMIN.value:
            return True
        return permission in self.get_permissions_list()

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


class AdminUser(Base):
    """管理员用户表"""

    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(100), nullable=True)  # 显示名称
    avatar = Column(String(500), nullable=True)  # 头像URL
    is_active = Column(Boolean, default=True)  # 是否激活
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_login_ip = Column(String(50), nullable=True)  # 最后登录IP
    login_count = Column(Integer, default=0)  # 登录次数
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 角色关联
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

    # 关联角色
    role = relationship("Role", back_populates="users")

    def set_password(self, password: str) -> None:
        """
        设置密码（自动哈希）

        Args:
            password: 明文密码
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
            "utf-8"
        )

    def verify_password(self, password: str) -> bool:
        """
        验证密码

        Args:
            password: 明文密码

        Returns:
            bool: 密码是否正确
        """
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def has_permission(self, permission: str) -> bool:
        """
        检查用户是否有特定权限

        Args:
            permission: 权限标识，如 'post:create'

        Returns:
            bool: 是否有权限
        """
        # 如果没有角色，拒绝所有权限
        if not self.role:
            return False

        # 超级管理员拥有所有权限
        if self.role.code == UserRole.SUPER_ADMIN.value:
            return True

        return self.role.has_permission(permission)

    def has_any_permission(self, permissions: list) -> bool:
        """
        检查用户是否有任意一个权限

        Args:
            permissions: 权限标识列表

        Returns:
            bool: 是否有任意一个权限
        """
        return any(self.has_permission(p) for p in permissions)

    def has_all_permissions(self, permissions: list) -> bool:
        """
        检查用户是否有所有权限

        Args:
            permissions: 权限标识列表

        Returns:
            bool: 是否有所有权限
        """
        return all(self.has_permission(p) for p in permissions)

    def get_role_name(self) -> str:
        """获取角色名称"""
        if self.role:
            return self.role.name
        return "无角色"

    def __repr__(self) -> str:
        return f"<AdminUser(id={self.id}, username='{self.username}')>"
