"""用户/会员系统模块 - User & Membership Module"""

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    """
    用户模型

    用于用户注册、登录、个人资料管理、角色权限、会员等级、积分系统
    """

    __tablename__ = "user"

    # 基本信息
    username = Column(String(100), unique=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, nullable=False, comment="邮箱")
    phone = Column(String(50), nullable=True, comment="手机号码")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")

    # 个人资料
    first_name = Column(String(50), nullable=True, comment="名字")
    last_name = Column(String(50), nullable=True, comment="姓氏")
    display_name = Column(String(100), nullable=True, comment="显示名称")
    bio = Column(Text, nullable=True, comment="个人简介")
    avatar_url = Column(String(255), nullable=True, comment="头像URL")
    date_of_birth = Column(DateTime, nullable=True, comment="出生日期")
    gender = Column(
        Enum("male", "female", "other", "prefer_not_to_say", name="user_gender"),
        nullable=True,
        comment="性别",
    )

    # 联系信息
    address_line1 = Column(String(255), nullable=True, comment="地址行1")
    address_line2 = Column(String(255), nullable=True, comment="地址行2")
    city = Column(String(100), nullable=True, comment="城市")
    state = Column(String(100), nullable=True, comment="州/省")
    postal_code = Column(String(20), nullable=True, comment="邮编")
    country = Column(String(100), nullable=True, default="New Zealand", comment="国家")

    # 角色与权限
    role = Column(
        Enum("admin", "member", "vip", "guest", name="user_role"),
        default="member",
        nullable=False,
        comment="用户角色",
    )
    is_active = Column(Boolean, default=True, nullable=False, comment="账户是否激活")
    is_verified = Column(Boolean, default=False, nullable=False, comment="邮箱是否已验证")
    is_staff = Column(Boolean, default=False, nullable=False, comment="是否为员工")

    # 会员等级系统
    membership_level = Column(
        Enum("basic", "silver", "gold", "platinum", name="membership_level"),
        default="basic",
        nullable=False,
        comment="会员等级",
    )
    membership_expires_at = Column(DateTime, nullable=True, comment="会员到期时间")

    # 积分系统
    points = Column(Integer, default=0, nullable=False, comment="用户积分")
    total_earned_points = Column(
        Integer, default=0, nullable=False, comment="累计获得积分"
    )

    # 登录与安全
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")
    last_login_ip = Column(String(50), nullable=True, comment="最后登录IP")
    login_count = Column(Integer, default=0, nullable=False, comment="登录次数")
    failed_login_attempts = Column(
        Integer, default=0, nullable=False, comment="失败登录次数"
    )
    locked_until = Column(DateTime, nullable=True, comment="账户锁定至")

    # 通知偏好
    email_notifications = Column(
        Boolean, default=True, nullable=False, comment="是否接收邮件通知"
    )
    sms_notifications = Column(
        Boolean, default=False, nullable=False, comment="是否接收短信通知"
    )
    marketing_emails = Column(
        Boolean, default=True, nullable=False, comment="是否接收营销邮件"
    )

    # 社交账号
    facebook_id = Column(String(100), nullable=True, comment="Facebook账号ID")
    google_id = Column(String(100), nullable=True, comment="Google账号ID")
    linkedin_id = Column(String(100), nullable=True, comment="LinkedIn账号ID")

    # 其他
    notes = Column(Text, nullable=True, comment="管理员备注")
    email_verified_at = Column(DateTime, nullable=True, comment="邮箱验证时间")
    phone_verified_at = Column(DateTime, nullable=True, comment="手机验证时间")

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"
