"""数据库模型基类"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr

from app.database import Base


class TimestampMixin:
    """时间戳混入类 - 为所有模型添加创建和更新时间"""

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
        )


class BaseModel(Base, TimestampMixin):
    """抽象基类模型"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
