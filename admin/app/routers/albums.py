"""
相册管理路由（后台）

提供完整的相册管理功能：
- 相册 CRUD
- 照片管理
- 相册分类管理
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.album import Album, AlbumCategory, AlbumPhoto
from app.models.media import MediaFile
from admin.app.services.album_service import AlbumService

# prefix 已在 main.py 中设置为 /admin/albums，这里不需要再加
router = APIRouter()
templates = Jinja2Templates(directory="admin/templates")


def get_album_service(db: Session = Depends(get_db)) -> AlbumService:
    """获取相册服务实例"""
    return AlbumService(db)


# ============================================================
# 页面路由
# ============================================================


@router.get("", response_class=HTMLResponse)
async def list_albums(
    request: Request,
    status: Optional[str] = None,
    category_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    album_service: AlbumService = Depends(get_album_service),
):
    """相册列表页面"""
    # 获取相册列表
    albums, total = album_service.get_albums(status, category_id, page, page_size)

    # 获取分类列表
    categories = album_service.get_categories()

    # 获取统计信息
    stats = album_service.get_statistics()

    # 计算总页数
    total_pages = (total + page_size - 1) // page_size

    return templates.TemplateResponse(
        "albums/list.html",
        {
            "request": request,
            "albums": albums,
            "categories": categories,
            "current_status": status or "all",
            "current_category_id": category_id,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "stats": stats,
        },
    )


@router.get("/new", response_class=HTMLResponse)
async def new_album(
    request: Request,
    db: Session = Depends(get_db),
    album_service: AlbumService = Depends(get_album_service),
):
    """新建相册页面"""
    categories = album_service.get_categories(enabled_only=True)

    return templates.TemplateResponse(
        "albums/form.html",
        {
            "request": request,
            "album": None,
            "categories": categories,
            "action": "create",
        },
    )


@router.get("/{album_id}/edit", response_class=HTMLResponse)
async def edit_album(
    request: Request,
    album_id: int,
    db: Session = Depends(get_db),
    album_service: AlbumService = Depends(get_album_service),
):
    """编辑相册页面"""
    album = album_service.get_album(album_id)
    if not album:
        raise HTTPException(status_code=404, detail="相册不存在")

    categories = album_service.get_categories(enabled_only=True)

    return templates.TemplateResponse(
        "albums/form.html",
        {
            "request": request,
            "album": album,
            "categories": categories,
            "action": "update",
        },
    )


@router.get("/{album_id}/photos", response_class=HTMLResponse)
async def manage_photos(
    request: Request,
    album_id: int,
    db: Session = Depends(get_db),
    album_service: AlbumService = Depends(get_album_service),
):
    """照片管理页面"""
    album = album_service.get_album(album_id)
    if not album:
        raise HTTPException(status_code=404, detail="相册不存在")

    # 获取所有可用的媒体文件（仅图片）
    available_media = (
        db.query(MediaFile)
        .filter(MediaFile.file_type == "image")
        .order_by(MediaFile.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        "albums/photos.html",
        {
            "request": request,
            "album": album,
            "available_media": available_media,
        },
    )


# ============================================================
# 相册 API
# ============================================================


@router.post("")
async def create_album(
    title: str = Form(...),
    slug: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    status: str = Form("draft"),
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    seo_keywords: Optional[str] = Form(None),
    album_service: AlbumService = Depends(get_album_service),
):
    """创建相册 API"""
    album, error = album_service.create_album(
        title=title,
        slug=slug,
        description=description,
        category_id=category_id,
        status=status,
        seo_title=seo_title,
        seo_description=seo_description,
        seo_keywords=seo_keywords,
    )

    if error:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return RedirectResponse(
        url=f"/admin/albums/{album.id}/edit", status_code=303
    )


@router.get("/{album_id}")
async def get_album(
    album_id: int, album_service: AlbumService = Depends(get_album_service)
):
    """获取相册详情 API"""
    album = album_service.get_album(album_id)
    if not album:
        return JSONResponse(
            status_code=404, content={"success": False, "message": "相册不存在"}
        )

    return JSONResponse(
        content={
            "success": True,
            "album": {
                "id": album.id,
                "title": album.title,
                "slug": album.slug,
                "description": album.description,
                "cover_url": album.cover_media.path_thumb if album.cover_media else None,
                "category_id": album.category_id,
                "category_name": album.category_name,
                "photo_count": album.photo_count,
                "view_count": album.view_count,
                "status": album.status,
                "created_at": album.created_at.isoformat(),
            },
        }
    )


@router.put("/{album_id}")
async def update_album(
    album_id: int,
    title: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    status: Optional[str] = Form(None),
    seo_title: Optional[str] = Form(None),
    seo_description: Optional[str] = Form(None),
    seo_keywords: Optional[str] = Form(None),
    album_service: AlbumService = Depends(get_album_service),
):
    """更新相册 API"""
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if slug is not None:
        update_data["slug"] = slug
    if description is not None:
        update_data["description"] = description
    if category_id is not None:
        update_data["category_id"] = category_id
    if status is not None:
        update_data["status"] = status
    if seo_title is not None:
        update_data["seo_title"] = seo_title
    if seo_description is not None:
        update_data["seo_description"] = seo_description
    if seo_keywords is not None:
        update_data["seo_keywords"] = seo_keywords

    success, error = album_service.update_album(album_id, **update_data)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "更新成功"})


@router.delete("/{album_id}")
async def delete_album(
    album_id: int, album_service: AlbumService = Depends(get_album_service)
):
    """删除相册 API"""
    success, error = album_service.delete_album(album_id)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "删除成功"})


@router.post("/{album_id}/publish")
async def publish_album(
    album_id: int, album_service: AlbumService = Depends(get_album_service)
):
    """发布/取消发布相册 API"""
    album = album_service.get_album(album_id)
    if not album:
        return JSONResponse(
            status_code=404, content={"success": False, "message": "相册不存在"}
        )

    if album.status == "published":
        success, error = album_service.unpublish_album(album_id)
        message = "已取消发布"
    else:
        success, error = album_service.publish_album(album_id)
        message = "已发布"

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": message})


# ============================================================
# 照片管理 API
# ============================================================


@router.post("/{album_id}/photos")
async def add_photo(
    album_id: int,
    request: Request,
    album_service: AlbumService = Depends(get_album_service),
):
    """添加照片 API"""
    data = await request.json()
    media_id = data.get("media_id")
    caption = data.get("caption")

    if not media_id:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "请选择照片"}
        )

    photo, error = album_service.add_photo(album_id, media_id, caption)

    if error:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "添加成功"})


@router.post("/{album_id}/photos/batch")
async def add_photos_batch(
    album_id: int,
    request: Request,
    album_service: AlbumService = Depends(get_album_service),
):
    """批量添加照片 API"""
    data = await request.json()
    media_ids = data.get("media_ids", [])

    if not media_ids:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "请选择照片"}
        )

    added_count, errors = album_service.add_photos_batch(album_id, media_ids)

    if errors:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"添加了 {added_count} 张照片，{len(errors)} 张失败",
                "errors": errors,
            },
        )

    return JSONResponse(
        content={"success": True, "message": f"成功添加 {added_count} 张照片"}
    )


@router.delete("/{album_id}/photos/{photo_id}")
async def remove_photo(
    album_id: int,
    photo_id: int,
    album_service: AlbumService = Depends(get_album_service),
):
    """移除照片 API"""
    success, error = album_service.remove_photo(album_id, photo_id)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "移除成功"})


@router.put("/photos/{photo_id}")
async def update_photo_caption(
    photo_id: int,
    caption: str = Form(...),
    album_service: AlbumService = Depends(get_album_service),
):
    """更新照片说明 API"""
    success, error = album_service.update_photo_caption(photo_id, caption)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "更新成功"})


@router.put("/{album_id}/photos/sort")
async def sort_photos(
    album_id: int,
    request: Request,
    album_service: AlbumService = Depends(get_album_service),
):
    """
    排序照片 API

    请求体: {
        "orders": [[photo_id, sort_order], ...]
    }
    """
    data = await request.json()
    orders = data.get("orders", [])

    if not orders:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "无效的排序数据"}
        )

    success, error = album_service.sort_photos(album_id, orders)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "排序成功"})


@router.post("/{album_id}/cover")
async def set_cover(
    album_id: int,
    request: Request,
    album_service: AlbumService = Depends(get_album_service),
):
    """设置封面 API"""
    data = await request.json()
    media_id = data.get("media_id")

    if not media_id:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "请选择封面图"}
        )

    success, error = album_service.set_cover(album_id, media_id)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "设置成功"})


# ============================================================
# 分类管理 API
# ============================================================


@router.get("/categories/list")
async def list_categories(album_service: AlbumService = Depends(get_album_service)):
    """获取分类列表 API"""
    categories = album_service.get_categories()

    return JSONResponse(
        content={
            "success": True,
            "categories": [
                {
                    "id": c.id,
                    "name": c.name,
                    "slug": c.slug,
                    "description": c.description,
                    "is_enabled": c.is_enabled,
                    "sort_order": c.sort_order,
                }
                for c in categories
            ],
        }
    )


@router.post("/categories")
async def create_category(
    name: str = Form(...),
    slug: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    album_service: AlbumService = Depends(get_album_service),
):
    """创建分类 API"""
    category, error = album_service.create_category(
        name=name, slug=slug, description=description
    )

    if error:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(
        content={
            "success": True,
            "message": "创建成功",
            "category": {"id": category.id, "name": category.name, "slug": category.slug},
        }
    )


@router.put("/categories/{category_id}")
async def update_category(
    category_id: int,
    name: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    is_enabled: Optional[bool] = Form(None),
    album_service: AlbumService = Depends(get_album_service),
):
    """更新分类 API"""
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if slug is not None:
        update_data["slug"] = slug
    if description is not None:
        update_data["description"] = description
    if is_enabled is not None:
        update_data["is_enabled"] = is_enabled

    success, error = album_service.update_category(category_id, **update_data)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "更新成功"})


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int, album_service: AlbumService = Depends(get_album_service)
):
    """删除分类 API"""
    success, error = album_service.delete_category(category_id)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "删除成功"})
