"""
回收站路由 - 软删除内容管理
"""

import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from admin.app.database import get_db
from app.models import Post, Product, Gallery, SiteColumn, SinglePage
from app.models.trash import TrashItem
from admin.app.dependencies import get_current_admin_user

router = APIRouter(tags=["trash"])


class TrashItemResponse(BaseModel):
    id: int
    content_type: str
    content_id: int
    original_data: dict
    deleted_at: str
    deleted_by: Optional[int]
    delete_reason: Optional[str]
    storage_size: int


class MoveToTrashRequest(BaseModel):
    content_type: str
    content_id: int
    reason: Optional[str] = None


class RestoreFromTrashRequest(BaseModel):
    trash_id: int


@router.get("/trash", response_class=HTMLResponse)
async def trash_page(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """回收站管理页面"""
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="admin/templates")

    # 获取回收站项目
    trash_items = (
        db.query(TrashItem)
        .order_by(TrashItem.deleted_at.desc())
        .all()
    )

    # 统计信息
    stats = {
        "total": len(trash_items),
        "posts": len([i for i in trash_items if i.content_type == "post"]),
        "products": len([i for i in trash_items if i.content_type == "product"]),
        "galleries": len([i for i in trash_items if i.content_type == "gallery"]),
        "columns": len([i for i in trash_items if i.content_type == "column"]),
        "pages": len([i for i in trash_items if i.content_type == "page"]),
    }

    # 格式化数据
    items = []
    for item in trash_items:
        data = json.loads(item.original_data)
        title = data.get("title") or data.get("name") or data.get("title_en") or "未知"
        items.append({
            "id": item.id,
            "content_type": item.content_type,
            "content_id": item.content_id,
            "title": title,
            "deleted_at": item.deleted_at.strftime("%Y-%m-%d %H:%M:%S"),
            "reason": item.delete_reason,
            "storage_size": item.storage_size,
        })

    return templates.TemplateResponse("trash.html", {
        "request": request,
        "items": items,
        "stats": stats,
    })


@router.get("/api/trash")
async def get_trash_list(
    content_type: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取回收站列表"""
    query = db.query(TrashItem)

    if content_type:
        query = query.filter(TrashItem.content_type == content_type)

    total = query.count()
    items = (
        query
        .order_by(TrashItem.deleted_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return JSONResponse(content={
        "success": True,
        "data": {
            "items": [
                {
                    "id": item.id,
                    "content_type": item.content_type,
                    "content_id": item.content_id,
                    "title": json.loads(item.original_data).get("title", ""),
                    "deleted_at": item.deleted_at.isoformat(),
                    "reason": item.delete_reason,
                }
                for item in items
            ],
            "total": total,
            "page": page,
            "limit": limit,
        }
    })


@router.post("/api/trash/move")
async def move_to_trash(
    request: MoveToTrashRequest,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """将内容移动到回收站"""
    try:
        original_data = {}
        content_type = request.content_type
        content_id = request.content_id

        # 获取原始数据
        if content_type == "post":
            item = db.query(Post).filter(Post.id == content_id).first()
            if item:
                original_data = {
                    "title": item.title,
                    "title_en": item.title_en,
                    "summary": item.summary,
                    "summary_en": item.summary_en,
                    "content_html": item.content_html,
                    "content_html_en": item.content_html_en,
                    "status": item.status,
                    "column_id": item.column_id,
                }
                # 软删除：更新状态
                item.status = "offline"
        elif content_type == "product":
            item = db.query(Product).filter(Product.id == content_id).first()
            if item:
                original_data = {
                    "name": item.name,
                    "name_en": item.name_en,
                    "description": item.description,
                    "description_en": item.description_en,
                    "status": item.status,
                }
                item.status = "offline"
        elif content_type == "gallery":
            item = db.query(Gallery).filter(Gallery.id == content_id).first()
            if item:
                original_data = {
                    "title": item.title,
                    "description": item.description,
                    "status": item.status,
                }
                item.status = "offline"
        elif content_type == "column":
            item = db.query(SiteColumn).filter(SiteColumn.id == content_id).first()
            if item:
                original_data = {
                    "name": item.name,
                    "name_en": item.name_en,
                    "slug": item.slug,
                    "description": item.description,
                    "status": item.status,
                }
                item.status = "offline"
        elif content_type == "page":
            item = db.query(SinglePage).filter(SinglePage.id == content_id).first()
            if item:
                original_data = {
                    "title": item.title,
                    "title_en": item.title_en,
                    "content_html": item.content_html,
                    "content_html_en": item.content_html_en,
                    "status": item.status,
                }
                item.status = "offline"
        else:
            raise HTTPException(status_code=400, detail="不支持的内容类型")

        if not original_data:
            raise HTTPException(status_code=404, detail="内容不存在")

        # 创建回收站记录
        trash_item = TrashItem(
            content_type=content_type,
            content_id=content_id,
            original_data=json.dumps(original_data, ensure_ascii=False, indent=2),
            deleted_at=datetime.now(),
            deleted_by=admin_user.id if admin_user else None,
            delete_reason=request.reason,
            storage_size=len(json.dumps(original_data)),
        )
        db.add(trash_item)
        db.commit()

        return JSONResponse(content={
            "success": True,
            "message": "已移动到回收站",
            "trash_id": trash_item.id
        })
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/trash/restore")
async def restore_from_trash(
    request: RestoreFromTrashRequest,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """从回收站恢复内容"""
    try:
        trash_item = (
            db.query(TrashItem)
            .filter(TrashItem.id == request.trash_id)
            .first()
        )

        if not trash_item:
            raise HTTPException(status_code=404, detail="回收站项目不存在")

        original_data = json.loads(trash_item.original_data)
        content_type = trash_item.content_type
        content_id = trash_item.content_id

        # 恢复原始数据
        if content_type == "post":
            item = db.query(Post).filter(Post.id == content_id).first()
            if item:
                item.title = original_data.get("title", item.title)
                item.title_en = original_data.get("title_en")
                item.summary = original_data.get("summary")
                item.summary_en = original_data.get("summary_en")
                item.content_html = original_data.get("content_html", "")
                item.content_html_en = original_data.get("content_html_en")
                item.status = original_data.get("status", "draft")
        elif content_type == "product":
            item = db.query(Product).filter(Product.id == content_id).first()
            if item:
                item.name = original_data.get("name", item.name)
                item.name_en = original_data.get("name_en")
                item.description = original_data.get("description")
                item.description_en = original_data.get("description_en")
                item.status = original_data.get("status", "draft")
        elif content_type == "gallery":
            item = db.query(Gallery).filter(Gallery.id == content_id).first()
            if item:
                item.title = original_data.get("title", item.title)
                item.description = original_data.get("description")
                item.status = original_data.get("status", "draft")
        elif content_type == "column":
            item = db.query(SiteColumn).filter(SiteColumn.id == content_id).first()
            if item:
                item.name = original_data.get("name", item.name)
                item.name_en = original_data.get("name_en")
                item.description = original_data.get("description")
                item.status = original_data.get("status", "draft")
        elif content_type == "page":
            item = db.query(SinglePage).filter(SinglePage.id == content_id).first()
            if item:
                item.title = original_data.get("title", item.title)
                item.title_en = original_data.get("title_en")
                item.content_html = original_data.get("content_html", "")
                item.content_html_en = original_data.get("content_html_en")
                item.status = original_data.get("status", "draft")

        # 删除回收站记录
        db.delete(trash_item)
        db.commit()

        return JSONResponse(content={
            "success": True,
            "message": "恢复成功"
        })
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/trash/{trash_id}")
async def delete_trash_item(
    trash_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """彻底删除回收站项目"""
    try:
        trash_item = (
            db.query(TrashItem)
            .filter(TrashItem.id == trash_id)
            .first()
        )

        if not trash_item:
            raise HTTPException(status_code=404, detail="回收站项目不存在")

        # 真正删除数据库中的内容
        content_type = trash_item.content_type
        content_id = trash_item.content_id

        if content_type == "post":
            db.query(Post).filter(Post.id == content_id).delete()
        elif content_type == "product":
            db.query(Product).filter(Product.id == content_id).delete()
        elif content_type == "gallery":
            db.query(Gallery).filter(Gallery.id == content_id).delete()
        elif content_type == "column":
            db.query(SiteColumn).filter(SiteColumn.id == content_id).delete()
        elif content_type == "page":
            db.query(SinglePage).filter(SinglePage.id == content_id).delete()

        # 删除回收站记录
        db.delete(trash_item)
        db.commit()

        return JSONResponse(content={
            "success": True,
            "message": "已彻底删除"
        })
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/trash/empty")
async def empty_trash(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """清空回收站"""
    try:
        # 获取所有回收站项目
        trash_items = db.query(TrashItem).all()

        # 逐个删除（确保关联删除）
        for trash_item in trash_items:
            content_type = trash_item.content_type
            content_id = trash_item.content_id

            if content_type == "post":
                db.query(Post).filter(Post.id == content_id).delete()
            elif content_type == "product":
                db.query(Product).filter(Product.id == content_id).delete()
            elif content_type == "gallery":
                db.query(Gallery).filter(Gallery.id == content_id).delete()
            elif content_type == "column":
                db.query(SiteColumn).filter(SiteColumn.id == content_id).delete()
            elif content_type == "page":
                db.query(SinglePage).filter(SinglePage.id == content_id).delete()

        # 清空回收站表
        db.query(TrashItem).delete()
        db.commit()

        return JSONResponse(content={
            "success": True,
            "message": f"已清空回收站，删除 {len(trash_items)} 个项目"
        })
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/trash/stats")
async def get_trash_stats(
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取回收站统计信息"""
    trash_items = db.query(TrashItem).all()

    stats = {
        "total": len(trash_items),
        "posts": len([i for i in trash_items if i.content_type == "post"]),
        "products": len([i for i in trash_items if i.content_type == "product"]),
        "galleries": len([i for i in trash_items if i.content_type == "gallery"]),
        "columns": len([i for i in trash_items if i.content_type == "column"]),
        "pages": len([i for i in trash_items if i.content_type == "page"]),
        "total_storage": sum(i.storage_size for i in trash_items),
    }

    return JSONResponse(content={
        "success": True,
        "data": stats
    })
