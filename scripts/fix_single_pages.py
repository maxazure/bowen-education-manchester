"""
批量修复单页数据
- 为缺失 slug 的单页生成 slug
- 将 content_html 转换为简化的 content_markdown
"""

import re
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services import single_page_service


def html_to_simple_markdown(html: str) -> str:
    """
    将简单的 HTML 转换为 Markdown

    Args:
        html: HTML 字符串

    Returns:
        Markdown 字符串
    """
    if not html:
        return ""

    # 去除外层的 div.container
    text = re.sub(r'<div[^>]*>', '', html)
    text = re.sub(r'</div>', '\n', text)

    # 转换标题
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n', text)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', text)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n', text)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n', text)

    # 转换段落
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text)

    # 转换强调
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text)

    # 转换链接
    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', text)

    # 转换列表
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text)
    text = re.sub(r'</?ul[^>]*>', '', text)
    text = re.sub(r'</?ol[^>]*>', '', text)

    # 转换换行
    text = re.sub(r'<br\s*/?>', '\n', text)

    # 清理多余的空行
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 去除首尾空白
    text = text.strip()

    return text


def main():
    """主函数"""
    # 连接数据库
    engine = create_engine('sqlite:///instance/database.db')
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        # 查询所有 slug 为空的单页
        from app.models.site import SinglePage
        pages = db.query(SinglePage).filter(
            (SinglePage.slug == None) | (SinglePage.slug == '')
        ).all()

        print(f"找到 {len(pages)} 个需要修复的单页")

        for page in pages:
            print(f"\n处理: {page.id} - {page.title}")

            # 生成 slug
            if not page.slug:
                slug = single_page_service.generate_slug(page.title, db, exclude_id=page.id)
                page.slug = slug
                print(f"  生成 slug: {slug}")

            # 转换 content_html 为 content_markdown
            if not page.content_markdown and page.content_html:
                markdown_content = html_to_simple_markdown(page.content_html)
                page.content_markdown = markdown_content
                print(f"  生成 Markdown (长度: {len(markdown_content)})")

            db.commit()

        print(f"\n✅ 成功修复 {len(pages)} 个单页")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
