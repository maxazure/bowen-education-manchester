"""团队展示模块 - Team Showcase Module"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class TeamMember(BaseModel):
    """
    团队成员模型

    用于展示企业团队成员、管理层、专家顾问等
    """

    __tablename__ = "team_member"

    name = Column(String(100), nullable=False, comment="姓名")
    title = Column(String(100), nullable=True, comment="职位/头衔")
    department = Column(String(100), nullable=True, comment="部门/团队")

    # 照片
    photo_media_id = Column(
        Integer, ForeignKey("media_file.id"), nullable=True, comment="照片ID"
    )

    # 简介和资质
    bio = Column(Text, nullable=True, comment="个人简介")
    qualifications = Column(Text, nullable=True, comment="专业资质与证书")
    specialties = Column(String(500), nullable=True, comment="专长领域")

    # 联系方式
    email = Column(String(100), nullable=True, comment="邮箱")
    phone = Column(String(50), nullable=True, comment="电话")
    linkedin = Column(String(255), nullable=True, comment="LinkedIn链接")
    twitter = Column(String(255), nullable=True, comment="Twitter链接")

    # 展示控制
    sort_order = Column(Integer, default=0, nullable=False, comment="排序序号")
    is_featured = Column(Boolean, default=False, nullable=False, comment="是否为核心成员")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否启用")

    # 关系
    photo = relationship("MediaFile", foreign_keys=[photo_media_id])
