# -*- coding: utf-8 -*-
"""
模板过滤器工具
用于双语模板系统的内容过滤
"""

import re
from typing import Optional


def remove_chinese(html: Optional[str]) -> str:
    """
    从HTML内容中移除中文内容

    用于纯英文模板版本，自动过滤掉标记为中文的内容

    Args:
        html: HTML内容字符串

    Returns:
        过滤后的HTML内容

    Examples:
        >>> html = '<p>Hello</p><p class="text-chinese">你好</p>'
        >>> remove_chinese(html)
        '<p>Hello</p>'
    """
    if not html:
        return ""

    # 移除带有 chinese 类名的标签及其内容
    # 匹配 <p class="text-chinese">...</p>
    # 匹配 <span class="chinese">...</span>
    # 匹配 <div class="chinese-content">...</div>
    html = re.sub(
        r'<([a-z][a-z0-9]*)\s+[^>]*class=["\'][^"\']*chinese[^"\']*["\'][^>]*>.*?</\1>',
        '',
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 移除 <br> 后面的独立中文段落
    # 例如: "English text<br>中文文本" -> "English text"
    html = re.sub(r'<br\s*/?\s*>[\s\r\n]*<span[^>]*>[\u4e00-\u9fff\s]+</span>', '', html, flags=re.IGNORECASE)

    # 移除换行符后的纯中文文本
    # 例如: "English\n中文" -> "English"
    html = re.sub(r'\n[\s]*[\u4e00-\u9fff\s、，。！？：；""''（）【】《》]+', '', html)

    # 清理多余的空白标签
    # 例如: "<p></p>", "<span></span>"
    html = re.sub(r'<([a-z][a-z0-9]*)\s*>\s*</\1>', '', html, flags=re.IGNORECASE)

    # 清理多余的连续<br>标签
    html = re.sub(r'(<br\s*/?\s*>){2,}', '<br>', html, flags=re.IGNORECASE)

    # 清理多余的空白行
    html = re.sub(r'\n{3,}', '\n\n', html)

    return html.strip()


def strip_chinese_text(text: Optional[str]) -> str:
    """
    从纯文本中移除所有中文字符

    警告：这个函数会移除所有中文字符，可能会影响混合内容
    建议优先使用 remove_chinese() 过滤HTML标记的内容

    Args:
        text: 纯文本字符串

    Returns:
        移除中文后的文本

    Examples:
        >>> strip_chinese_text("Hello 你好 World")
        "Hello  World"
    """
    if not text:
        return ""

    # 移除中文字符（包括常用标点）
    text = re.sub(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+', '', text)

    # 清理多余空白
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def format_bilingual_title(title: Optional[str], lang: str = 'en') -> str:
    """
    格式化双语标题

    从包含中英文的标题中提取对应语言的部分

    Args:
        title: 原始标题（可能包含中英文）
        lang: 目标语言 ('en' 或 'zh')

    Returns:
        格式化后的标题

    Examples:
        >>> format_bilingual_title("About Us 关于我们", "en")
        "About Us"
        >>> format_bilingual_title("About Us 关于我们", "zh")
        "About Us 关于我们"
    """
    if not title:
        return ""

    if lang == 'en':
        # 移除中文部分
        # 尝试按分隔符分割
        if ' | ' in title:
            parts = title.split(' | ')
            # 返回第一个非中文部分
            for part in parts:
                if not re.search(r'[\u4e00-\u9fff]', part):
                    return part.strip()

        # 移除括号中的中文
        title = re.sub(r'\s*[（(][\u4e00-\u9fff\s]+[)）]', '', title)

        # 移除尾部的中文
        title = re.sub(r'\s+[\u4e00-\u9fff\s]+$', '', title)

        return title.strip()

    # 中文版保持原样
    return title


def get_lang_specific_content(content_dict: dict, lang: str, field_base: str) -> Optional[str]:
    """
    从字典中获取特定语言的内容

    Args:
        content_dict: 包含多语言内容的字典
        lang: 目标语言代码 ('en' 或 'zh')
        field_base: 字段基础名称（如 'content', 'description'）

    Returns:
        对应语言的内容，如果不存在则返回默认内容

    Examples:
        >>> data = {'content_en': 'Hello', 'content_zh': '你好', 'content': 'Default'}
        >>> get_lang_specific_content(data, 'en', 'content')
        'Hello'
    """
    if not content_dict:
        return None

    # 尝试获取特定语言字段
    lang_field = f"{field_base}_{lang}"
    if lang_field in content_dict and content_dict[lang_field]:
        return content_dict[lang_field]

    # 尝试获取英文字段（作为备选）
    if lang == 'zh' and f"{field_base}_en" in content_dict:
        return content_dict[f"{field_base}_en"]

    # 返回默认字段
    if field_base in content_dict:
        return content_dict[field_base]

    return None


# 导出所有过滤器
__all__ = [
    'remove_chinese',
    'strip_chinese_text',
    'format_bilingual_title',
    'get_lang_specific_content',
]
