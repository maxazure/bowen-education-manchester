#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建统一页面布局相关数据表：page_layout、page_layout_section、page_layout_block

运行方式：
    source venv/bin/activate
    python scripts/migrate_homepage_layout.py
"""

from app.database import engine
from app.models import site  # 保证依赖的表已加载（site_column）
from app.models.layout import PageLayout, PageLayoutSection, PageLayoutBlock
from sqlalchemy import MetaData


def ensure_tables():
    metadata = MetaData()
    # 收集目标表的元数据
    for tbl in [PageLayout.__table__, PageLayoutSection.__table__, PageLayoutBlock.__table__]:
        tbl.metadata = metadata
    # 使用各模型自身的 metadata 创建（直接使用模型定义的 Base metadata 更简洁）
    PageLayout.metadata.create_all(bind=engine, tables=[
        PageLayout.__table__, PageLayoutSection.__table__, PageLayoutBlock.__table__
    ])


if __name__ == "__main__":
    print("[migrate] Creating layout tables if not exist...")
    ensure_tables()
    print("[migrate] Done.")