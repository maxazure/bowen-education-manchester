"""访问统计管理路由"""

import re
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import PageVisit, VisitLog, VisitSummary

router = APIRouter(tags=["analytics"])


def detect_device_type(user_agent: str) -> str:
    """检测设备类型"""
    ua = user_agent.lower()
    if 'mobile' in ua or 'android' in ua:
        return 'mobile'
    elif 'tablet' in ua or 'ipad' in ua:
        return 'tablet'
    return 'desktop'


def detect_browser(user_agent: str) -> str:
    """检测浏览器"""
    ua = user_agent.lower()
    if 'chrome' in ua:
        return 'Chrome'
    elif 'firefox' in ua:
        return 'Firefox'
    elif 'safari' in ua:
        return 'Safari'
    elif 'edge' in ua:
        return 'Edge'
    elif 'msie' in ua or 'trident' in ua:
        return 'IE'
    return 'Other'


def detect_os(user_agent: str) -> str:
    """检测操作系统"""
    ua = user_agent.lower()
    if 'windows' in ua:
        return 'Windows'
    elif 'mac os' in ua:
        return 'macOS'
    elif 'iphone' in ua or 'ipad' in ua:
        return 'iOS'
    elif 'android' in ua:
        return 'Android'
    elif 'linux' in ua:
        return 'Linux'
    return 'Other'


@router.get("/analytics", response_class=HTMLResponse)
async def analytics_page(
    request: Request,
    days: int = 7,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """访问统计页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # 整体统计
    total_visits = db.query(func.sum(PageVisit.visit_count)).scalar() or 0
    today_visits = db.query(func.coalesce(func.sum(VisitLog.id), 0)).filter(
        VisitLog.visit_time >= end_date.replace(hour=0, minute=0, second=0)
    ).scalar() or 0

    # 热门页面
    top_pages = (
        db.query(PageVisit)
        .order_by(desc(PageVisit.visit_count))
        .limit(10)
        .all()
    )

    # 最近访问记录
    recent_logs = (
        db.query(VisitLog)
        .order_by(desc(VisitLog.visit_time))
        .limit(20)
        .all()
    )

    # 按天的访问趋势
    daily_stats = (
        db.query(
            func.date(VisitLog.visit_time).label('date'),
            func.count(VisitLog.id).label('visits')
        )
        .filter(VisitLog.visit_time >= start_date)
        .group_by(func.date(VisitLog.visit_time))
        .order_by('date')
        .all()
    )

    # 设备分布
    device_stats = (
        db.query(
            VisitLog.device_type,
            func.count(VisitLog.id).label('count')
        )
        .filter(VisitLog.visit_time >= start_date)
        .group_by(VisitLog.device_type)
        .all()
    )

    # 浏览器分布
    browser_stats = (
        db.query(
            VisitLog.browser,
            func.count(VisitLog.id).label('count')
        )
        .filter(VisitLog.visit_time >= start_date)
        .group_by(VisitLog.browser)
        .order_by(desc('count'))
        .limit(5)
        .all()
    )

    # 计算总页面数
    total_pages = db.query(PageVisit).count()

    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "stats": {
            "total_visits": total_visits,
            "today_visits": today_visits,
            "total_pages": total_pages,
            "days": days,
        },
        "top_pages": top_pages,
        "recent_logs": recent_logs,
        "daily_stats": daily_stats,
        "device_stats": device_stats,
        "browser_stats": browser_stats,
    })


@router.get("/api/analytics/tracking.js")
async def tracking_script():
    """返回网站跟踪脚本"""
    script = """
(function() {
    var pageData = {
        path: window.location.pathname,
        title: document.title,
        referrer: document.referrer,
        timestamp: new Date().toISOString()
    };

    // 发送访问数据
    fetch('/api/analytics/track', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(pageData)
    }).catch(function() {});
})();
"""
    return HTMLResponse(content=script, media_type="application/javascript")


@router.post("/api/analytics/track")
async def track_visit(
    request: Request,
    db: Session = Depends(get_db),
):
    """记录页面访问"""
    try:
        data = await request.json()
        page_path = data.get('path', '/')
        page_title = data.get('title', '')

        # 清理路径
        page_path = page_path[:500] if page_path else '/'

        # 获取用户信息
        user_agent = request.headers.get('user-agent', '')
        referer = request.headers.get('referer', '')

        # 解析IP（简化处理）
        client_ip = request.client.host if request.client else ''

        # 检测设备信息
        device_type = detect_device_type(user_agent)
        browser = detect_browser(user_agent)
        os = detect_os(user_agent)

        # 更新或创建页面访问统计
        page_visit = db.query(PageVisit).filter(PageVisit.page_path == page_path).first()
        if page_visit:
            page_visit.visit_count += 1
            page_visit.last_visited_at = datetime.now()
        else:
            page_visit = PageVisit(
                page_path=page_path,
                page_title=page_title,
                visit_count=1,
                last_visited_at=datetime.now()
            )
            db.add(page_visit)

        # 创建访问日志
        visit_log = VisitLog(
            page_path=page_path,
            page_title=page_title,
            referer=referer[:1000] if referer else '',
            user_agent=user_agent[:500] if user_agent else '',
            ip_address=client_ip,
            device_type=device_type,
            browser=browser,
            os=os,
            visit_time=datetime.now()
        )
        db.add(visit_log)

        db.commit()

        return JSONResponse(content={"success": True})
    except Exception as e:
        db.rollback()
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@router.get("/api/analytics/stats")
async def get_analytics_stats(
    days: int = 7,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user) = None,
):
    """获取统计数据 API"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # 总访问量
    total_visits = db.query(func.sum(PageVisit.visit_count)).scalar() or 0

    # 今日访问
    today_visits = db.query(func.count(VisitLog.id)).filter(
        VisitLog.visit_time >= end_date.replace(hour=0, minute=0, second=0)
    ).scalar() or 0

    # 本周访问
    week_start = end_date - timedelta(days=end_date.weekday())
    week_visits = db.query(func.count(VisitLog.id)).filter(
        VisitLog.visit_time >= week_start
    ).scalar() or 0

    # 热门页面
    top_pages = (
        db.query(PageVisit)
        .order_by(desc(PageVisit.visit_count))
        .limit(10)
        .all()
    )

    # 按天的趋势
    daily_trend = (
        db.query(
            func.date(VisitLog.visit_time).label('date'),
            func.count(VisitLog.id).label('visits')
        )
        .filter(VisitLog.visit_time >= start_date)
        .group_by(func.date(VisitLog.visit_time))
        .order_by('date')
        .all()
    )

    # 设备分布
    devices = (
        db.query(
            VisitLog.device_type,
            func.count(VisitLog.id).label('count')
        )
        .filter(VisitLog.visit_time >= start_date)
        .group_by(VisitLog.device_type)
        .all()
    )

    return JSONResponse(content={
        "success": True,
        "data": {
            "total_visits": total_visits,
            "today_visits": today_visits,
            "week_visits": week_visits,
            "days": days,
            "top_pages": [
                {"path": p.page_path, "title": p.page_title, "visits": p.visit_count}
                for p in top_pages
            ],
            "daily_trend": [
                {"date": str(d[0]), "visits": d[1]}
                for d in daily_trend
            ],
            "devices": [
                {"type": d[0], "count": d[1]}
                for d in devices
            ]
        }
    })


@router.get("/api/analytics/top-pages")
async def get_top_pages(
    limit: int = 10,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user) = None,
):
    """获取热门页面 API"""
    top_pages = (
        db.query(PageVisit)
        .order_by(desc(PageVisit.visit_count))
        .limit(limit)
        .all()
    )

    return JSONResponse(content={
        "success": True,
        "data": [
            {
                "id": p.id,
                "path": p.page_path,
                "title": p.page_title,
                "visits": p.visit_count,
                "last_visited": p.last_visited_at.isoformat() if p.last_visited_at else None
            }
            for p in top_pages
        ]
    })


@router.get("/api/analytics/hourly")
async def get_hourly_stats(
    days: int = 7,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user) = None,
):
    """获取小时访问分布 API"""
    from sqlalchemy import extract

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    hourly_stats = (
        db.query(
            extract('hour', VisitLog.visit_time).label('hour'),
            func.count(VisitLog.id).label('count')
        )
        .filter(VisitLog.visit_time >= start_date)
        .group_by(extract('hour', VisitLog.visit_time))
        .order_by('hour')
        .all()
    )

    return JSONResponse(content={
        "success": True,
        "data": [
            {"hour": int(h[0]), "count": h[1]}
            for h in hourly_stats
        ]
    })


@router.get("/api/analytics/os-distribution")
async def get_os_distribution(
    days: int = 7,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user) = None,
):
    """获取操作系统分布 API"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    os_stats = (
        db.query(
            VisitLog.os,
            func.count(VisitLog.id).label('count')
        )
        .filter(VisitLog.visit_time >= start_date)
        .group_by(VisitLog.os)
        .order_by(desc('count'))
        .limit(10)
        .all()
    )

    return JSONResponse(content={
        "success": True,
        "data": [
            {"os": o[0], "count": o[1]}
            for o in os_stats
        ]
    })


@router.get("/api/analytics/compare")
async def get_comparison_stats(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user) = None,
):
    """获取对比统计 API - 本周 vs 上周"""
    now = datetime.now()
    this_week_start = now - timedelta(days=now.weekday())
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start

    this_week_visits = db.query(func.count(VisitLog.id)).filter(
        VisitLog.visit_time >= this_week_start
    ).scalar() or 0

    last_week_visits = db.query(func.count(VisitLog.id)).filter(
        VisitLog.visit_time >= last_week_start,
        VisitLog.visit_time < last_week_end
    ).scalar() or 0

    # 文章对比
    from app.models import Post
    this_month_posts = db.query(func.count(Post.id)).filter(
        Post.created_at >= now.replace(day=1, hour=0, minute=0, second=0)
    ).scalar() or 0

    last_month = now.replace(day=1) - timedelta(days=1)
    last_month_posts = db.query(func.count(Post.id)).filter(
        Post.created_at >= last_month.replace(day=1),
        Post.created_at < now.replace(day=1)
    ).scalar() or 0

    return JSONResponse(content={
        "success": True,
        "data": {
            "this_week_visits": this_week_visits,
            "last_week_visits": last_week_visits,
            "visit_change": ((this_week_visits - last_week_visits) / max(last_week_visits, 1) * 100),
            "this_month_posts": this_month_posts,
            "last_month_posts": last_month_posts,
            "post_change": ((this_month_posts - last_month_posts) / max(last_month_posts, 1) * 100) if last_month_posts > 0 else 0
        }
    })
