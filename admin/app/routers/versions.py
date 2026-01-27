"""
内容版本历史路由

管理内容的版本历史和回滚功能
"""

import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import ContentVersion, Post, Product, Gallery, AdminUser

router = APIRouter(tags=["versions"])


@router.get("/versions", response_class=HTMLResponse)
async def versions_page(
    request: Request,
    content_type: str = "post",
    content_id: Optional[int] = None,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """版本历史页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 获取内容列表
    if content_type == "post":
        items = db.query(Post).order_by(desc(Post.created_at)).limit(20).all()
    elif content_type == "product":
        items = db.query(Product).order_by(desc(Product.created_at)).limit(20).all()
    elif content_type == "gallery":
        items = db.query(Gallery).order_by(desc(Gallery.created_at)).limit(20).all()
    else:
        items = []

    # 如果指定了内容ID，获取该内容的版本历史
    versions = []
    if content_id:
        versions = db.query(ContentVersion).filter(
            ContentVersion.content_type == content_type,
            ContentVersion.content_id == content_id
        ).order_by(desc(ContentVersion.version_number)).limit(50).all()

    return templates.TemplateResponse("versions.html", {
        "request": request,
        "content_type": content_type,
        "content_id": content_id,
        "items": items,
        "versions": versions,
    })


@router.get("/api/versions/{content_type}/{content_id}")
async def get_versions(
    content_type: str,
    content_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取内容版本历史"""
    valid_types = ["post", "product", "gallery"]
    if content_type not in valid_types:
        return JSONResponse(
            content={"success": False, "message": "不支持的内容类型"},
            status_code=400
        )

    query = db.query(ContentVersion).filter(
        ContentVersion.content_type == content_type,
        ContentVersion.content_id == content_id
    )

    total = query.count()
    versions = query.order_by(desc(ContentVersion.version_number)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return JSONResponse(content={
        "success": True,
        "data": {
            "items": [
                {
                    "id": v.id,
                    "version_number": v.version_number,
                    "title": v.title,
                    "action": v.action,
                    "admin_name": v.admin_name,
                    "remark": v.remark,
                    "created_at": v.created_at.isoformat() if v.created_at else None,
                }
                for v in versions
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    })


@router.get("/api/versions/{version_id}")
async def get_version_detail(
    version_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取版本详情"""
    version = db.query(ContentVersion).filter(ContentVersion.id == version_id).first()

    if not version:
        return JSONResponse(
            content={"success": False, "message": "版本不存在"},
            status_code=404
        )

    return JSONResponse(content={
        "success": True,
        "data": {
            "id": version.id,
            "content_type": version.content_type,
            "content_id": version.content_id,
            "version_number": version.version_number,
            "title": version.title,
            "content_snapshot": version.content_snapshot,
            "action": version.action,
            "admin_name": version.admin_name,
            "remark": version.remark,
            "created_at": version.created_at.isoformat() if version.created_at else None,
        }
    })


@router.post("/api/versions/{version_id}/restore")
async def restore_version(
    version_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """回滚到指定版本"""
    version = db.query(ContentVersion).filter(ContentVersion.id == version_id).first()

    if not version:
        return JSONResponse(
            content={"success": False, "message": "版本不存在"},
            status_code=404
        )

    # 获取当前内容
    if version.content_type == "post":
        content = db.query(Post).filter(Post.id == version.content_id).first()
    elif version.content_type == "product":
        content = db.query(Product).filter(Product.id == version.content_id).first()
    elif version.content_type == "gallery":
        content = db.query(Gallery).filter(Gallery.id == version.content_id).first()
    else:
        return JSONResponse(
            content={"success": False, "message": "不支持的内容类型"},
            status_code=400
        )

    if not content:
        return JSONResponse(
            content={"success": False, "message": "原始内容不存在"},
            status_code=404
        )

    # 保存当前状态为新版本
    current_snapshot = json.dumps({
        "title": content.title if hasattr(content, 'title') else content.name,
        "content_html": content.content_html if hasattr(content, 'content_html') else None,
    }, ensure_ascii=False, default=str)

    new_version = ContentVersion(
        content_type=version.content_type,
        content_id=version.content_id,
        version_number=db.query(func.max(ContentVersion.version_number)).filter(
            ContentVersion.content_type == version.content_type,
            ContentVersion.content_id == version.content_id
        ).scalar() or 0 + 1,
        title=f"回滚前备份: {content.title[:30] if hasattr(content, 'title') else content.name[:30]}",
        content_snapshot=current_snapshot,
        action="backup_before_restore",
        admin_id=admin_user.id,
        admin_name=admin_user.username,
        remark=f"回滚到版本 {version.version_number} 前的自动备份",
    )
    db.add(new_version)

    # 恢复版本内容
    try:
        snapshot = json.loads(version.content_snapshot) if version.content_snapshot else {}
        if hasattr(content, 'title'):
            content.title = snapshot.get("title", "")
        if hasattr(content, 'name'):
            content.name = snapshot.get("name", "")
        if hasattr(content, 'content_html'):
            content.content_html = snapshot.get("content_html", "")
    except (json.JSONDecodeError, TypeError):
        pass

    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": f"已成功回滚到版本 {version.version_number}",
        "data": {
            "restored_version": version.version_number,
            "backup_version": new_version.version_number,
        }
    })


@router.post("/api/versions/cleanup")
async def cleanup_versions(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """清理旧版本"""
    data = await request.json()
    content_type = data.get("content_type")
    content_id = data.get("content_id")
    keep_count = data.get("keep_count", 10)

    if not content_type or not content_id:
        return JSONResponse(
            content={"success": False, "message": "缺少必要参数"},
            status_code=400
        )

    # 获取要删除的版本
    subquery = db.query(ContentVersion.id).filter(
        ContentVersion.content_type == content_type,
        ContentVersion.content_id == content_id
    ).order_by(desc(ContentVersion.version_number)).offset(keep_count).subquery()

    deleted = db.query(ContentVersion).filter(
        ContentVersion.id.in_(subquery)
    ).delete(synchronize_session=False)

    db.commit()

    return JSONResponse(content={
        "success": True,
        "message": f"已清理 {deleted} 个旧版本，保留最近 {keep_count} 个版本"
    })


@router.get("/api/content/versions")
async def get_content_with_versions(
    content_type: str = "post",
    limit: int = 20,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取有版本历史的内容列表"""
    # 获取有版本的内容ID
    version_content_ids = db.query(
        ContentVersion.content_type,
        ContentVersion.content_id,
        func.max(ContentVersion.created_at).label('latest_version')
    ).filter(
        ContentVersion.content_type == content_type
    ).group_by(
        ContentVersion.content_type,
        ContentVersion.content_id
    ).order_by(
        desc('latest_version')
    ).limit(limit).all()

    results = []
    for vc in version_content_ids:
        content_id = vc.content_id

        # 获取内容标题
        if content_type == "post":
            content = db.query(Post).filter(Post.id == content_id).first()
            title = content.title if content else "未知"
        elif content_type == "product":
            content = db.query(Product).filter(Product.id == content_id).first()
            title = content.name if content else "未知"
        else:
            content = db.query(Gallery).filter(Gallery.id == content_id).first()
            title = content.title if content else "未知"

        # 获取版本数量
        version_count = db.query(func.count(ContentVersion.id)).filter(
            ContentVersion.content_type == content_type,
            ContentVersion.content_id == content_id
        ).scalar()

        results.append({
            "content_type": content_type,
            "content_id": content_id,
            "title": title,
            "version_count": version_count,
            "latest_version": vc.latest_version.isoformat() if vc.latest_version else None,
        })

    return JSONResponse(content={
        "success": True,
        "data": results
    })


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="admin/templates")
