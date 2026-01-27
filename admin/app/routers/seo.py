"""
SEO分析工具路由

内容SEO分析和优化建议
"""

import re
from typing import Optional, List, Dict
from collections import Counter

from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import func, desc, or_
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import Post, Product, Gallery, SiteColumn

router = APIRouter(tags=["seo"])


@router.get("/seo", response_class=HTMLResponse)
async def seo_page(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """SEO分析页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 获取SEO统计
    posts = db.query(Post).all()

    # 计算整体SEO评分
    total_score = 0
    analyzed_count = 0
    issues = {"critical": 0, "warning": 0, "info": 0}

    for post in posts:
        score, post_issues = analyze_post_seo(post)
        total_score += score
        analyzed_count += 1
        issues["critical"] += post_issues["critical"]
        issues["warning"] += post_issues["warning"]
        issues["info"] += post_issues["info"]

    avg_score = round(total_score / analyzed_count, 1) if analyzed_count else 0

    # 获取有问题的内容
    problematic_posts = []
    for post in posts:
        score, post_issues = analyze_post_seo(post)
        if score < 60:
            problematic_posts.append({
                "id": post.id,
                "title": post.title[:40],
                "score": score,
                "issues": post_issues["critical"] + post_issues["warning"],
            })

    return templates.TemplateResponse("seo.html", {
        "request": request,
        "stats": {
            "total_posts": len(posts),
            "avg_score": avg_score,
            "issues": issues,
            "problematic_count": len(problematic_posts),
        },
        "problematic_posts": problematic_posts[:10],
    })


@router.get("/api/seo/analyze/{content_type}/{content_id}")
async def analyze_content(
    content_type: str,
    content_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """分析单个内容的SEO"""
    if content_type == "post":
        content = db.query(Post).filter(Post.id == content_id).first()
    elif content_type == "product":
        content = db.query(Product).filter(Product.id == content_id).first()
    else:
        return JSONResponse(
            content={"success": False, "message": "不支持的内容类型"},
            status_code=400
        )

    if not content:
        return JSONResponse(
            content={"success": False, "message": "内容不存在"},
            status_code=404
        )

    analysis = analyze_seo(content, content_type)

    return JSONResponse(content={
        "success": True,
        "data": analysis
    })


@router.get("/api/seo/list")
async def get_seo_list(
    content_type: str = "post",
    sort_by: str = "score",
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取内容SEO列表"""
    if content_type == "post":
        items = db.query(Post).all()
    elif content_type == "product":
        items = db.query(Product).all()
    else:
        return JSONResponse(
            content={"success": False, "message": "不支持的内容类型"},
            status_code=400
        )

    # 分析每个内容
    analyzed_items = []
    for item in items:
        analysis = analyze_seo(item, content_type)
        analyzed_items.append({
            "id": item.id,
            "title": item.title[:40] if hasattr(item, 'title') else item.name[:40],
            "score": analysis["score"],
            "issues_count": len(analysis["issues"]),
            "status": analysis["status"],
        })

    # 排序
    if sort_by == "score":
        analyzed_items.sort(key=lambda x: x["score"])
    elif sort_by == "issues":
        analyzed_items.sort(key=lambda x: x["issues_count"], reverse=True)

    # 分页
    total = len(analyzed_items)
    start = (page - 1) * page_size
    end = start + page_size

    return JSONResponse(content={
        "success": True,
        "data": {
            "items": analyzed_items[start:end],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    })


@router.get("/api/seo/keywords")
async def get_keyword_stats(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取关键词统计"""
    posts = db.query(Post).filter(Post.status == 'published').all()

    # 提取所有标题中的关键词
    words = []
    stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '个', '吗', '吧', '呢', '啊', '哦', '嗯', '怎样', '如何', '什么', '为什么', '吗'}

    for post in posts:
        if post.title:
            # 提取中文字符
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', post.title)
            words.extend([c for c in chinese_chars if c not in stop_words])

    # 统计词频
    word_counts = Counter(words)
    top_keywords = word_counts.most_common(30)

    return JSONResponse(content={
        "success": True,
        "data": [
            {"keyword": word, "count": count}
            for word, count in top_keywords
        ]
    })


def analyze_seo(content, content_type):
    """分析内容的SEO"""
    issues = []
    score = 100

    # 标题分析
    title = content.title if hasattr(content, 'title') else (content.name or "")
    title_len = len(title)

    if content_type == "post" or content_type == "product":
        seo_title = content.seo_title or ""
        seo_desc = content.seo_description or ""
    else:
        seo_title = getattr(content, 'seo_title', '') or ''
        seo_desc = getattr(content, 'seo_description', '') or ''

    # 标题长度检查
    if title_len < 10:
        issues.append({
            "type": "title",
            "level": "warning",
            "message": f"标题太短 ({title_len} 字符)，建议至少10个字符",
            "suggestion": "增加标题长度，使其更具描述性"
        })
        score -= 5
    elif title_len > 60:
        issues.append({
            "type": "title",
            "level": "warning",
            "message": f"标题太长 ({title_len} 字符)，建议不超过60字符",
            "suggestion": "精简标题，突出核心关键词"
        })
        score -= 5

    # SEO标题检查
    if not seo_title:
        issues.append({
            "type": "seo_title",
            "level": "critical",
            "message": "缺少SEO标题",
            "suggestion": "为页面设置SEO标题，包含核心关键词"
        })
        score -= 15
    elif len(seo_title) > 60:
        issues.append({
            "type": "seo_title",
            "level": "warning",
            "message": f"SEO标题过长 ({len(seo_title)} 字符)",
            "suggestion": "将SEO标题控制在60字符以内"
        })
        score -= 3

    # SEO描述检查
    if not seo_desc:
        issues.append({
            "type": "seo_description",
            "level": "critical",
            "message": "缺少SEO描述",
            "suggestion": "为页面设置SEO描述，包含核心关键词"
        })
        score -= 15
    else:
        desc_len = len(seo_desc)
        if desc_len < 50:
            issues.append({
                "type": "seo_description",
                "level": "warning",
                "message": f"SEO描述太短 ({desc_len} 字符)，建议50-160字符",
                "suggestion": "增加描述内容，更好地概括页面内容"
            })
            score -= 5
        elif desc_len > 160:
            issues.append({
                "type": "seo_description",
                "level": "warning",
                "message": f"SEO描述太长 ({desc_len} 字符)，建议不超过160字符",
                "suggestion": "精简描述，突出核心卖点"
            })
            score -= 3

    # 内容检查
    if content_type == "post":
        content_html = content.content_html or ""
    else:
        content_html = getattr(content, 'description_html', '') or getattr(content, 'content_html', '') or ''

    word_count = len(re.findall(r'\w+', content_html))

    if word_count < 300:
        issues.append({
            "type": "content",
            "level": "warning",
            "message": f"内容过短 ({word_count} 字)，建议至少300字",
            "suggestion": "增加内容深度，提供更多有价值信息"
        })
        score -= 10

    # 图片ALT检查
    img_count = len(re.findall(r'<img[^>]*>', content_html, re.IGNORECASE))
    alt_count = len(re.findall(r'alt=["\']([^"\']+)["\']', content_html, re.IGNORECASE))

    if img_count > 0 and img_count != alt_count:
        missing = img_count - alt_count
        issues.append({
            "type": "images",
            "level": "warning",
            "message": f"{missing} 张图片缺少alt属性",
            "suggestion": "为所有图片添加alt描述，提高可访问性和SEO"
        })
        score -= 5

    # 链接检查
    links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>', content_html, re.IGNORECASE)
    external_links = [l for l in links if l.startswith('http') and 'bowen-education' not in l]

    if len(external_links) > 5:
        issues.append({
            "type": "links",
            "level": "info",
            "message": f"外部链接较多 ({len(external_links)} 个)",
            "suggestion": "控制外部链接数量，优先使用内部链接"
        })
        score -= 2

    # 关键词检查
    if seo_title or seo_desc:
        keywords = set(re.findall(r'[\w]+', (seo_title + seo_desc).lower()))
        title_words = set(re.findall(r'[\w]+', title.lower()))
        missing_keywords = keywords - title_words

        if missing_keywords and len(missing_keywords) > 2:
            issues.append({
                "type": "keywords",
                "level": "info",
                "message": "SEO标题/描述中部分关键词未出现在正文中",
                "suggestion": "在正文中自然融入核心关键词"
            })
            score -= 2

    # 确定状态
    if score >= 80:
        status = "good"
    elif score >= 60:
        status = "ok"
    else:
        status = "poor"

    return {
        "score": max(0, score),
        "status": status,
        "issues": issues,
        "checks": {
            "title": {"length": title_len, "valid": 10 <= title_len <= 60},
            "seo_title": {"length": len(seo_title), "valid": 0 < len(seo_title) <= 60},
            "seo_description": {"length": len(seo_desc), "valid": 50 <= len(seo_desc) <= 160},
            "content_words": {"count": word_count, "valid": word_count >= 300},
            "images_alt": {"total": img_count, "with_alt": alt_count, "valid": img_count == alt_count},
        }
    }


def analyze_post_seo(post):
    """快速分析文章SEO（用于列表展示）"""
    issues = {"critical": 0, "warning": 0, "info": 0}

    title = post.title or ""
    title_len = len(title)

    if title_len < 10 or title_len > 60:
        issues["warning"] += 1

    if not post.seo_title:
        issues["critical"] += 1
    elif len(post.seo_title) > 60:
        issues["warning"] += 1

    if not post.seo_description:
        issues["critical"] += 1

    content = post.content_html or ""
    word_count = len(re.findall(r'\w+', content))
    if word_count < 300:
        issues["warning"] += 1

    score = 100
    score -= issues["critical"] * 15
    score -= issues["warning"] * 5
    score -= issues["info"] * 2

    return max(0, score), issues


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="admin/templates")


@router.get("/api/seo-analysis")
async def get_seo_analysis(db: Session = Depends(get_db)):
    """获取所有文章的 SEO 分析"""
    posts = db.query(Post).all()

    if not posts:
        return {
            "success": True,
            "data": {
                "posts": [],
                "stats": {"total": 0, "excellent": 0, "good": 0, "warning": 0, "critical": 0},
                "commonIssues": []
            }
        }

    analyses = []
    for post in posts:
        analysis = analyze_post_seo_detailed(post)
        analyses.append(analysis)

    # 统计
    excellent = sum(1 for a in analyses if a["score"] >= 80)
    good = sum(1 for a in analyses if 60 <= a["score"] < 80)
    warning = sum(1 for a in analyses if 40 <= a["score"] < 60)
    critical = sum(1 for a in analyses if a["score"] < 40)

    # 常见问题统计
    all_issues = []
    for a in analyses:
        all_issues.extend(a["issues"])

    issue_counts = Counter(all_issues)
    common_issues = [
        {"description": issue, "count": count}
        for issue, count in issue_counts.most_common(5)
    ]

    # 按评分排序
    analyses.sort(key=lambda x: x["score"])

    return {
        "success": True,
        "data": {
            "posts": analyses,
            "stats": {
                "total": len(analyses),
                "excellent": excellent,
                "good": good,
                "warning": warning,
                "critical": critical
            },
            "commonIssues": common_issues
        }
    }


def analyze_post_seo_detailed(post: Post) -> Dict[str, Any]:
    """详细分析单篇文章的 SEO"""
    issues = []
    suggestions = []

    # 标题分析
    title = post.title or ""
    title_length = len(title)
    if title_length < 30:
        issues.append("标题太短，建议 30-60 字符")
        suggestions.append("将标题扩展到至少 30 个字符")
    elif title_length > 60:
        issues.append("标题太长，建议不超过 60 字符")
        suggestions.append("精简标题到 60 字符以内")

    # 描述分析
    description = post.seo_description or post.summary or ""
    desc_length = len(description)
    if desc_length < 120:
        issues.append("SEO 描述太短，建议 120-160 字符")
        suggestions.append("添加更详细的 SEO 描述")
    elif desc_length > 160:
        issues.append("SEO 描述太长，建议不超过 160 字符")
        suggestions.append("精简 SEO 描述到 160 字符以内")

    # 关键词检查
    has_keywords = bool(post.seo_title or post.seo_description)
    if not has_keywords:
        issues.append("未设置 SEO 标题或描述")
        suggestions.append("为文章设置 SEO 标题和描述")

    # 图片 Alt 检查
    content = post.content_html or ""
    has_alt = 'alt="' in content
    if not has_alt and content.count('<img') > 0:
        issues.append("文章中的图片缺少 Alt 属性")
        suggestions.append("为所有图片添加 Alt 描述")

    # 内链检查
    internal_links = content.count('href="/') + content.count('href=\'/')
    if internal_links < 2:
        suggestions.append("建议添加更多站内链接")

    # 计算评分
    score = 100
    score -= min(30, len(issues) * 10)
    if not has_keywords:
        score -= 15
    if title_length < 30 or title_length > 60:
        score -= 10
    if desc_length < 120 or desc_length > 160:
        score -= 10

    score = max(0, min(100, score))

    return {
        "id": post.id,
        "title": post.title,
        "score": score,
        "titleLength": title_length,
        "descLength": desc_length,
        "hasKeywords": has_keywords,
        "hasAlt": has_alt,
        "internalLinks": internal_links,
        "issues": issues[:3],
        "suggestions": suggestions[:3],
        "mainIssue": issues[0] if issues else None
    }
