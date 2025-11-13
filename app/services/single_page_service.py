"""
单页服务层

提供单页相关的业务逻辑:
- Markdown 转 HTML
- Slug 生成
- 删除检查
"""

import re
from datetime import datetime
from typing import Optional, Tuple

import bleach
import markdown
from pypinyin import lazy_pinyin
from sqlalchemy.orm import Session

from app.models.site import SinglePage

# 允许的 HTML 标签和属性 (用于 bleach 清洗)
ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "code",
    "em",
    "i",
    "li",
    "ol",
    "pre",
    "strong",
    "ul",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "br",
    "span",
    "div",
    "img",
    "hr",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt", "title", "width", "height"],
    "span": ["class"],
    "div": ["class"],
    "code": ["class"],
    "pre": ["class"],
}


def markdown_to_html(content: str) -> str:
    """
    将 Markdown 转换为 HTML,并清洗 XSS

    Args:
        content: Markdown 文本

    Returns:
        安全的 HTML 文本
    """
    if not content:
        return ""

    # 转换 Markdown 为 HTML
    # 启用常用扩展: fenced_code, tables, nl2br
    html = markdown.markdown(
        content, extensions=["fenced_code", "tables", "nl2br", "codehilite"]
    )

    # 使用 bleach 清洗 HTML,防止 XSS 攻击
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,  # 移除不允许的标签
    )

    return clean_html


def slugify(text: str) -> str:
    """
    将文本转换为 URL 友好的 slug

    Args:
        text: 输入文本

    Returns:
        slug 字符串
    """
    if not text:
        return ""

    # 转为小写
    text = text.lower()

    # 如果包含中文,转换为拼音
    if re.search(r"[\u4e00-\u9fff]", text):
        # 使用 pypinyin 转换中文为拼音
        pinyin_list = lazy_pinyin(text)
        text = "-".join(pinyin_list)

    # 只保留字母、数字、连字符
    text = re.sub(r"[^\w\s-]", "", text)

    # 将空格替换为连字符
    text = re.sub(r"[-\s]+", "-", text)

    # 去除首尾连字符
    text = text.strip("-")

    return text


def generate_slug(title: str, db: Session, exclude_id: Optional[int] = None) -> str:
    """
    生成唯一的 slug

    Args:
        title: 页面标题
        db: 数据库会话
        exclude_id: 排除的页面 ID (用于更新时)

    Returns:
        唯一的 slug
    """
    base_slug = slugify(title)

    if not base_slug:
        base_slug = "page"

    # 检查 slug 是否已存在
    query = db.query(SinglePage).filter(SinglePage.slug == base_slug)
    if exclude_id:
        query = query.filter(SinglePage.id != exclude_id)

    existing = query.first()

    if not existing:
        return base_slug

    # 如果已存在,添加数字后缀
    counter = 1
    while True:
        new_slug = f"{base_slug}-{counter}"
        query = db.query(SinglePage).filter(SinglePage.slug == new_slug)
        if exclude_id:
            query = query.filter(SinglePage.id != exclude_id)

        if not query.first():
            return new_slug

        counter += 1


def can_delete_page(db: Session, page_id: int) -> Tuple[bool, str]:
    """
    检查页面是否可以删除

    Args:
        db: 数据库会话
        page_id: 页面 ID

    Returns:
        (是否可以删除, 错误消息)
    """
    page = db.query(SinglePage).filter(SinglePage.id == page_id).first()

    if not page:
        return False, "页面不存在"

    # 单页可以直接删除,无需特殊检查
    # 如果将来有引用关系(如评论),可以在这里添加检查
    return True, ""


def publish_page(db: Session, page_id: int) -> Tuple[bool, str]:
    """
    发布页面

    Args:
        db: 数据库会话
        page_id: 页面 ID

    Returns:
        (是否成功, 消息)
    """
    page = db.query(SinglePage).filter(SinglePage.id == page_id).first()

    if not page:
        return False, "页面不存在"

    if page.status == "published":
        return False, "页面已经是发布状态"

    page.status = "published"
    page.published_at = datetime.now()
    db.commit()

    return True, "发布成功"


def unpublish_page(db: Session, page_id: int) -> Tuple[bool, str]:
    """
    取消发布页面

    Args:
        db: 数据库会话
        page_id: 页面 ID

    Returns:
        (是否成功, 消息)
    """
    page = db.query(SinglePage).filter(SinglePage.id == page_id).first()

    if not page:
        return False, "页面不存在"

    if page.status == "draft":
        return False, "页面已经是草稿状态"

    page.status = "draft"
    db.commit()

    return True, "取消发布成功"
