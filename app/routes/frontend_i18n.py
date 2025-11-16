# -*- coding: utf-8 -*-
"""
Frontend I18n Routes
双语模板系统的路由扩展
"""

import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.utils.template_filters import (
    remove_chinese,
    format_bilingual_title,
    strip_chinese_text,
)

logger = logging.getLogger("docms")

router = APIRouter()


def get_template_engine(lang: str = "zh") -> Jinja2Templates:
    """
    根据语言代码返回对应的模板引擎

    Args:
        lang: 语言代码 ('zh' 或 'en')

    Returns:
        配置好的 Jinja2Templates 实例
    """
    # 确定模板目录
    template_base = Path(settings.template_dir)
    lang_dir = template_base / lang

    # 验证目录存在
    if not lang_dir.exists():
        logger.warning(f"Template directory {lang_dir} not found, falling back to zh")
        lang_dir = template_base / "zh"

    # 创建模板引擎
    templates = Jinja2Templates(directory=str(lang_dir))

    # 添加栏目名称本地化过滤器
    def get_column_name(column, lang_code=None):
        """获取栏目的本地化名称"""
        use_lang = lang_code or lang
        if use_lang == "en" and hasattr(column, 'name_en') and column.name_en:
            return column.name_en
        return column.name if hasattr(column, 'name') else str(column)

    templates.env.filters["column_name"] = get_column_name

    # 为英文模板添加过滤器
    if lang == "en":
        templates.env.filters["remove_chinese"] = remove_chinese
        templates.env.filters["format_title"] = lambda title: format_bilingual_title(title, "en")
        templates.env.filters["strip_chinese"] = strip_chinese_text

    # 为中文模板添加过滤器（保持原样）
    if lang == "zh":
        templates.env.filters["format_title"] = lambda title: format_bilingual_title(title, "zh")

    # 添加语言信息到全局变量
    templates.env.globals["current_lang"] = lang
    templates.env.globals["site_language"] = lang

    # 添加模板辅助函数
    from app.utils.template_helpers import (
        get_navigation,
        post_list,
        product_list,
        site_info,
    )
    templates.env.globals.update(
        {
            "product_list": product_list,
            "post_list": post_list,
            "site_info": site_info,
            "get_navigation": get_navigation,
        }
    )

    return templates


def get_lang_from_path(path: str) -> tuple[str, str]:
    """
    从URL路径中提取语言代码

    Args:
        path: URL路径，如 "/en/about" 或 "/about"

    Returns:
        (lang_code, clean_path) 元组
        - lang_code: 语言代码 ('en' 或 'zh')
        - clean_path: 移除语言前缀后的路径

    Examples:
        >>> get_lang_from_path("/en/about")
        ('en', '/about')
        >>> get_lang_from_path("/about")
        ('zh', '/about')
        >>> get_lang_from_path("/zh/school")
        ('zh', '/school')
    """
    # 移除开头的斜杠
    path = path.lstrip("/")

    # 检查是否以语言代码开头
    if path.startswith("en/") or path == "en":
        return ("en", "/" + path[3:] if len(path) > 3 else "/")
    elif path.startswith("zh/") or path == "zh":
        return ("zh", "/" + path[3:] if len(path) > 3 else "/")

    # 默认为中文版
    return ("zh", "/" + path if path else "/")


# 注意：这个文件定义了辅助函数，但不直接注册路由
# 路由将在 frontend.py 中使用这些函数
