"""操作日志模型"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from app.database import Base
from app.models.base import BaseModel


class OperationLog(BaseModel):
    """
    操作日志模型

    记录管理员的所有操作行为
    """
    __tablename__ = "operation_log"

    # 操作信息
    admin_user_id = Column(Integer, nullable=True, comment="管理员ID")
    admin_username = Column(String(100), nullable=True, comment="管理员用户名")
    action = Column(String(50), nullable=False, comment="操作类型: create, update, delete, login, logout, etc.")
    module = Column(String(50), nullable=False, comment="操作模块: post, product, column, etc.")

    # 操作对象
    target_type = Column(String(50), nullable=True, comment="目标类型: post, product, column, etc.")
    target_id = Column(Integer, nullable=True, comment="目标ID")
    target_name = Column(String(200), nullable=True, comment="目标名称")

    # 操作详情
    description = Column(String(500), nullable=True, comment="操作描述")
    old_data = Column(JSON, nullable=True, comment="操作前数据")
    new_data = Column(JSON, nullable=True, comment="操作后数据")

    # 访问信息
    ip_address = Column(String(45), nullable=True, comment="IP地址")
    user_agent = Column(String(500), nullable=True, comment="User Agent")

    # 状态
    status = Column(String(20), default="success", nullable=False, comment="状态: success, failed")
    error_message = Column(Text, nullable=True, comment="错误信息")

    def __repr__(self):
        return f"<OperationLog {self.action}:{self.module}>"
