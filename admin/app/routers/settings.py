"""
站点设置路由

提供站点设置的查看和更新功能
"""

from typing import Dict, Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.services.site_settings_service import (get_all_settings, update_settings)

router = APIRouter(tags=["settings"])
templates = Jinja2Templates(directory="admin/templates")


@router.get("", response_class=HTMLResponse)
async def settings_page(request: Request, db: Session = Depends(get_db)):
    """
    站点设置页面

    显示所有站点设置项，按 Tab 分组组织

    Args:
        request: FastAPI request 对象
        db: 数据库会话

    Returns:
        站点设置页面 HTML
    """
    # 获取所有设置
    all_settings = get_all_settings(db)

    # 准备默认值（如果设置不存在）
    default_settings = {
        # 基本信息
        "site_name": "",
        "site_tagline": "",
        "site_description": "",
        "logo_id": "",
        "favicon_id": "",
        # 联系方式
        "contact_phone": "",
        "contact_email": "",
        "contact_address": "",
        "contact_hours": "",
        # 社交媒体
        "social_wechat": "",
        "social_weibo": "",
        "social_facebook": "",
        "social_twitter": "",
        "social_linkedin": "",
        # 高级设置
        "seo_keywords": "",
        "seo_description": "",
        "analytics_code": "",
        "tracking_code": "",
    }

    # 合并默认值和实际设置
    settings = {**default_settings, **all_settings}

    return templates.TemplateResponse(
        "settings/index.html",
        {
            "request": request,
            "settings": settings,
        },
    )


@router.post("", response_class=JSONResponse)
async def update_settings_api(
    request: Request,
    db: Session = Depends(get_db),
    # 基本信息
    site_name: Optional[str] = Form(None),
    site_tagline: Optional[str] = Form(None),
    site_description: Optional[str] = Form(None),
    logo_id: Optional[str] = Form(None),
    favicon_id: Optional[str] = Form(None),
    # 联系方式
    contact_phone: Optional[str] = Form(None),
    contact_email: Optional[str] = Form(None),
    contact_address: Optional[str] = Form(None),
    contact_hours: Optional[str] = Form(None),
    # 社交媒体
    social_wechat: Optional[str] = Form(None),
    social_weibo: Optional[str] = Form(None),
    social_facebook: Optional[str] = Form(None),
    social_twitter: Optional[str] = Form(None),
    social_linkedin: Optional[str] = Form(None),
    # 高级设置
    seo_keywords: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    analytics_code: Optional[str] = Form(None),
    tracking_code: Optional[str] = Form(None),
):
    """
    更新站点设置

    批量更新所有站点设置项

    Args:
        request: FastAPI request 对象
        db: 数据库会话
        其他参数: 各个设置项

    Returns:
        JSON 响应，包含成功或失败信息
    """
    try:
        # 准备设置数据（只包含非 None 的值）
        settings_data: Dict[str, str] = {}

        # 基本信息
        if site_name is not None:
            settings_data["site_name"] = site_name
        if site_tagline is not None:
            settings_data["site_tagline"] = site_tagline
        if site_description is not None:
            settings_data["site_description"] = site_description
        if logo_id is not None:
            settings_data["logo_id"] = logo_id
        if favicon_id is not None:
            settings_data["favicon_id"] = favicon_id

        # 联系方式
        if contact_phone is not None:
            settings_data["contact_phone"] = contact_phone
        if contact_email is not None:
            settings_data["contact_email"] = contact_email
        if contact_address is not None:
            settings_data["contact_address"] = contact_address
        if contact_hours is not None:
            settings_data["contact_hours"] = contact_hours

        # 社交媒体
        if social_wechat is not None:
            settings_data["social_wechat"] = social_wechat
        if social_weibo is not None:
            settings_data["social_weibo"] = social_weibo
        if social_facebook is not None:
            settings_data["social_facebook"] = social_facebook
        if social_twitter is not None:
            settings_data["social_twitter"] = social_twitter
        if social_linkedin is not None:
            settings_data["social_linkedin"] = social_linkedin

        # 高级设置
        if seo_keywords is not None:
            settings_data["seo_keywords"] = seo_keywords
        if seo_description is not None:
            settings_data["seo_description"] = seo_description
        if analytics_code is not None:
            settings_data["analytics_code"] = analytics_code
        if tracking_code is not None:
            settings_data["tracking_code"] = tracking_code

        # 批量更新设置
        update_settings(db, settings_data)

        return JSONResponse(
            content={"success": True, "message": "设置已保存"},
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"保存失败: {str(e)}"},
            status_code=500,
        )
