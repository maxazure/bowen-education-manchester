#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态页面生成日志模型

记录静态页面生成的历史和详情
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from datetime import datetime


class StaticGenerationLog(BaseModel):
    """静态生成日志表"""
    __tablename__ = "static_generation_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    generation_type = Column(String(20), nullable=False)  # 'full' 或 'partial'
    total_pages = Column(Integer, default=0)
    successful_pages = Column(Integer, default=0)
    failed_pages = Column(Integer, default=0)
    start_time = Column(DateTime, nullable=False, default=datetime.now)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(20), default='running')  # 'running', 'completed', 'failed', 'partial'
    error_message = Column(Text, nullable=True)

    # 关系
    details = relationship(
        "StaticGenerationDetail",
        back_populates="log",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<StaticGenerationLog(id={self.id}, type={self.generation_type}, status={self.status})>"


class StaticGenerationDetail(BaseModel):
    """页面生成详情表"""
    __tablename__ = "static_generation_detail"

    id = Column(Integer, primary_key=True, autoincrement=True)
    log_id = Column(Integer, ForeignKey('static_generation_log.id'), nullable=False)
    page_type = Column(String(20), nullable=False)  # 'home', 'product', 'post', 'single_page', 'event'
    page_id = Column(Integer, nullable=True)  # 页面ID（首页为NULL）
    language = Column(String(5), nullable=False)  # 'zh' 或 'en'
    url_path = Column(String(500), nullable=False)  # URL路径
    file_path = Column(String(500), nullable=False)  # 文件路径
    status = Column(String(20), default='success')  # 'success', 'failed'
    error_message = Column(Text, nullable=True)
    generation_time = Column(Float, nullable=True)  # 生成耗时（秒）

    # 关系
    log = relationship("StaticGenerationLog", back_populates="details")

    def __repr__(self):
        return f"<StaticGenerationDetail(id={self.id}, type={self.page_type}, status={self.status})>"
