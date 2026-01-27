"""访问统计模型"""

from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Index
from app.models.base import BaseModel


class PageVisit(BaseModel):
    """页面访问记录"""
    __tablename__ = "page_visits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    page_path = Column(String(500), nullable=False, index=True)  # 页面路径
    page_title = Column(String(255))  # 页面标题
    visit_count = Column(BigInteger, default=0)  # 访问次数
    last_visited_at = Column(DateTime)  # 最后访问时间

    __table_args__ = (
        Index('idx_page_path', 'page_path'),
    )


class VisitLog(BaseModel):
    """访问日志（详细记录）"""
    __tablename__ = "visit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    page_path = Column(String(500), nullable=False, index=True)
    page_title = Column(String(255))
    referer = Column(String(1000))  # 来源页面
    user_agent = Column(String(500))  # 浏览器标识
    ip_address = Column(String(45))  # IP地址
    country = Column(String(100))  # 国家
    city = Column(String(100))  # 城市
    device_type = Column(String(20))  # 设备类型: desktop, mobile, tablet
    browser = Column(String(50))  # 浏览器
    os = Column(String(50))  # 操作系统
    visit_time = Column(DateTime, index=True)  # 访问时间

    __table_args__ = (
        Index('idx_visit_time_page', 'visit_time', 'page_path'),
    )


class VisitSummary(BaseModel):
    """每日访问汇总"""
    __tablename__ = "visit_summaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, index=True)  # 日期
    page_path = Column(String(500), nullable=False)  # 页面路径
    page_title = Column(String(255))
    visit_count = Column(BigInteger, default=0)  # 访问次数
    unique_visitors = Column(BigInteger, default=0)  # 独立访客数

    __table_args__ = (
        Index('idx_date_page', 'date', 'page_path', unique=True),
    )
