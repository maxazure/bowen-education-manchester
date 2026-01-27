"""
媒体库管理路由（扩展版）

提供完整的媒体文件管理功能：
- 文件上传（图片、视频、文档）
- 文件夹管理
- 图片编辑（裁剪、缩放、压缩）
- 文件批量操作
"""

from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from admin.app.database import get_db
from app.models.media import MediaFile, MediaFolder
from admin.app.services.media_service import MediaService

# prefix 已在 main.py 中设置为 /admin/media，这里不需要再加
router = APIRouter()
templates = Jinja2Templates(directory="admin/templates")


def get_media_service(db: Session = Depends(get_db)) -> MediaService:
    """获取媒体服务实例"""
    return MediaService(db)


# ============================================================
# 页面路由
# ============================================================


@router.get("", response_class=HTMLResponse)
async def list_media(
    request: Request,
    folder_id: Optional[int] = None,
    file_type: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 24,
    db: Session = Depends(get_db),
):
    """
    媒体库列表页面
    """
    # 构建查询
    query = db.query(MediaFile).options(joinedload(MediaFile.folder))

    # 文件夹筛选
    if folder_id:
        query = query.filter(MediaFile.folder_id == folder_id)

    # 文件类型筛选
    if file_type and file_type != "all":
        query = query.filter(MediaFile.file_type == file_type)

    # 搜索
    if search:
        query = query.filter(
            (MediaFile.filename_original.contains(search))
            | (MediaFile.title.contains(search))
        )

    # 排序
    query = query.order_by(MediaFile.created_at.desc())

    # 统计
    total_files = query.count()
    total_images = db.query(MediaFile).filter(MediaFile.file_type == "image").count()
    total_videos = db.query(MediaFile).filter(MediaFile.file_type == "video").count()
    total_documents = (
        db.query(MediaFile).filter(MediaFile.file_type == "document").count()
    )

    # 分页
    offset = (page - 1) * page_size
    files = query.offset(offset).limit(page_size).all()

    # 获取文件夹列表
    folders = db.query(MediaFolder).order_by(MediaFolder.sort_order).all()

    # 计算总页数
    total_pages = (total_files + page_size - 1) // page_size

    return templates.TemplateResponse(
        "media/list.html",
        {
            "request": request,
            "files": files,
            "folders": folders,
            "current_folder_id": folder_id,
            "current_file_type": file_type or "all",
            "search": search or "",
            "page": page,
            "page_size": page_size,
            "total": total_files,
            "total_pages": total_pages,
            "total_files": total_files,
            "total_images": total_images,
            "total_videos": total_videos,
            "total_documents": total_documents,
        },
    )


@router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request, db: Session = Depends(get_db)):
    """上传页面"""
    folders = db.query(MediaFolder).order_by(MediaFolder.sort_order).all()

    return templates.TemplateResponse(
        "media/upload.html",
        {
            "request": request,
            "folders": folders,
        },
    )


# ============================================================
# 文件 API
# ============================================================


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    folder_id: Optional[int] = Form(None),
    title: Optional[str] = Form(None),
    alt_text: Optional[str] = Form(None),
    caption: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    media_service: MediaService = Depends(get_media_service),
):
    """上传文件 API"""
    # 上传文件
    media_file, error = await media_service.upload_file(
        file, folder_id=folder_id, uploaded_by="admin"
    )

    if error:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    # 更新可选字段
    if title:
        media_file.title = title
    if alt_text:
        media_file.alt_text = alt_text
    if caption:
        media_file.caption = caption

    db.commit()
    db.refresh(media_file)

    return JSONResponse(
        content={
            "success": True,
            "message": "上传成功",
            "file": {
                "id": media_file.id,
                "filename": media_file.filename_original,
                "url": media_file.path_original,
                "thumb_url": media_file.path_thumb,
                "file_type": media_file.file_type,
                "size": media_file.size_formatted,
            },
        }
    )


@router.get("/{media_id}")
async def get_media(media_id: int, db: Session = Depends(get_db)):
    """获取文件详情 API"""
    media_file = (
        db.query(MediaFile)
        .options(joinedload(MediaFile.folder))
        .filter(MediaFile.id == media_id)
        .first()
    )

    if not media_file:
        return JSONResponse(
            status_code=404, content={"success": False, "message": "文件不存在"}
        )

    # 增加查看次数
    media_file.view_count += 1
    db.commit()

    return JSONResponse(
        content={
            "success": True,
            "file": {
                "id": media_file.id,
                "filename": media_file.filename_original,
                "title": media_file.title,
                "alt_text": media_file.alt_text,
                "caption": media_file.caption,
                "description": media_file.description,
                "file_type": media_file.file_type,
                "mime_type": media_file.mime_type,
                "size": media_file.size_formatted,
                "size_bytes": media_file.size_bytes,
                "width": media_file.width,
                "height": media_file.height,
                "url": media_file.path_original,
                "thumb_url": media_file.path_thumb,
                "medium_url": media_file.path_medium,
                "folder_id": media_file.folder_id,
                "folder_name": media_file.folder.name if media_file.folder else None,
                "tags": media_file.tags,
                "usage_count": media_file.usage_count,
                "view_count": media_file.view_count,
                "download_count": media_file.download_count,
                "created_at": media_file.created_at.isoformat(),
            },
        }
    )


@router.put("/{media_id}")
async def update_media(
    media_id: int,
    title: Optional[str] = Form(None),
    alt_text: Optional[str] = Form(None),
    caption: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    folder_id: Optional[int] = Form(None),
    tags: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """更新文件信息 API"""
    media_file = db.query(MediaFile).filter(MediaFile.id == media_id).first()

    if not media_file:
        return JSONResponse(
            status_code=404, content={"success": False, "message": "文件不存在"}
        )

    # 更新字段
    if title is not None:
        media_file.title = title
    if alt_text is not None:
        media_file.alt_text = alt_text
    if caption is not None:
        media_file.caption = caption
    if description is not None:
        media_file.description = description
    if folder_id is not None:
        media_file.folder_id = folder_id
    if tags is not None:
        media_file.tags = tags

    db.commit()
    db.refresh(media_file)

    return JSONResponse(content={"success": True, "message": "更新成功"})


@router.delete("/{media_id}")
async def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    media_service: MediaService = Depends(get_media_service),
):
    """删除文件 API"""
    success, error = media_service.delete_file(media_id)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "删除成功"})


@router.post("/batch-delete")
async def batch_delete_media(
    request: Request,
    db: Session = Depends(get_db),
    media_service: MediaService = Depends(get_media_service),
):
    """批量删除文件 API"""
    data = await request.json()
    media_ids = data.get("media_ids", [])

    if not media_ids:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "请选择要删除的文件"}
        )

    deleted_count = 0
    errors = []

    for media_id in media_ids:
        success, error = media_service.delete_file(media_id)
        if success:
            deleted_count += 1
        else:
            errors.append(f"ID {media_id}: {error}")

    if errors:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"删除了 {deleted_count} 个文件，{len(errors)} 个失败",
                "errors": errors,
            },
        )

    return JSONResponse(
        content={"success": True, "message": f"成功删除 {deleted_count} 个文件"}
    )


# ============================================================
# 图片编辑 API
# ============================================================


@router.post("/{media_id}/crop")
async def crop_image(
    media_id: int,
    request: Request,
    db: Session = Depends(get_db),
    media_service: MediaService = Depends(get_media_service),
):
    """裁剪图片 API"""
    data = await request.json()
    x = data.get("x", 0)
    y = data.get("y", 0)
    width = data.get("width")
    height = data.get("height")

    if not width or not height:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "请指定裁剪尺寸"}
        )

    success, error = media_service.crop_image(media_id, x, y, width, height)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "裁剪成功"})


@router.post("/{media_id}/resize")
async def resize_image(
    media_id: int,
    request: Request,
    db: Session = Depends(get_db),
    media_service: MediaService = Depends(get_media_service),
):
    """缩放图片 API"""
    data = await request.json()
    width = data.get("width")
    height = data.get("height")

    if not width or not height:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "请指定缩放尺寸"}
        )

    success, error = media_service.resize_image(media_id, width, height)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "缩放成功"})


@router.post("/{media_id}/compress")
async def compress_image(
    media_id: int,
    quality: int = Form(85),
    db: Session = Depends(get_db),
    media_service: MediaService = Depends(get_media_service),
):
    """压缩图片 API"""
    if not 1 <= quality <= 100:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "压缩质量必须在 1-100 之间"},
        )

    success, error = media_service.compress_image(media_id, quality)

    if not success:
        return JSONResponse(
            status_code=400, content={"success": False, "message": error}
        )

    return JSONResponse(content={"success": True, "message": "压缩成功"})


# ============================================================
# 文件夹管理 API
# ============================================================


@router.get("/folders/list")
async def list_folders(db: Session = Depends(get_db)):
    """获取文件夹列表 API"""
    folders = db.query(MediaFolder).order_by(MediaFolder.sort_order).all()

    return JSONResponse(
        content={
            "success": True,
            "folders": [
                {
                    "id": f.id,
                    "name": f.name,
                    "parent_id": f.parent_id,
                    "path": f.path,
                    "description": f.description,
                    "sort_order": f.sort_order,
                }
                for f in folders
            ],
        }
    )


@router.post("/folders")
async def create_folder(
    name: str = Form(...),
    parent_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """创建文件夹 API"""
    # 生成路径
    if parent_id:
        parent = db.query(MediaFolder).filter(MediaFolder.id == parent_id).first()
        if not parent:
            return JSONResponse(
                status_code=404, content={"success": False, "message": "父文件夹不存在"}
            )
        path = f"{parent.path}/{name}".replace("//", "/")
    else:
        path = f"/{name}"

    # 创建文件夹
    folder = MediaFolder(
        name=name,
        parent_id=parent_id,
        path=path,
        description=description,
    )

    db.add(folder)
    db.commit()
    db.refresh(folder)

    return JSONResponse(
        content={
            "success": True,
            "message": "创建成功",
            "folder": {
                "id": folder.id,
                "name": folder.name,
                "path": folder.path,
            },
        }
    )


@router.put("/folders/{folder_id}")
async def update_folder(
    folder_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """更新文件夹 API"""
    folder = db.query(MediaFolder).filter(MediaFolder.id == folder_id).first()

    if not folder:
        return JSONResponse(
            status_code=404, content={"success": False, "message": "文件夹不存在"}
        )

    if name:
        folder.name = name
        # 更新路径
        if folder.parent_id:
            parent = (
                db.query(MediaFolder).filter(MediaFolder.id == folder.parent_id).first()
            )
            folder.path = f"{parent.path}/{name}".replace("//", "/")
        else:
            folder.path = f"/{name}"

    if description is not None:
        folder.description = description

    db.commit()
    db.refresh(folder)

    return JSONResponse(content={"success": True, "message": "更新成功"})


@router.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int, db: Session = Depends(get_db)):
    """删除文件夹 API"""
    folder = db.query(MediaFolder).filter(MediaFolder.id == folder_id).first()

    if not folder:
        return JSONResponse(
            status_code=404, content={"success": False, "message": "文件夹不存在"}
        )

    # 检查是否有子文件夹或文件
    has_children = db.query(MediaFolder).filter(MediaFolder.parent_id == folder_id).first()
    has_files = db.query(MediaFile).filter(MediaFile.folder_id == folder_id).first()

    if has_children or has_files:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "文件夹不为空，无法删除"},
        )

    db.delete(folder)
    db.commit()

    return JSONResponse(content={"success": True, "message": "删除成功"})


@router.get("/api/list")
async def list_media_api(
    folder_id: Optional[int] = None,
    file_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """获取媒体文件列表 API（供其他页面调用）"""
    import os
    from datetime import datetime

    # 查询数据库中的文件
    query = db.query(MediaFile)

    if folder_id:
        query = query.filter(MediaFile.folder_id == folder_id)

    if file_type:
        query = query.filter(MediaFile.type == file_type)

    total = query.count()
    files = query.order_by(MediaFile.created_at.desc()).offset(offset).limit(limit).all()

    # 获取文件夹信息
    folders = db.query(MediaFolder).all()

    # 构建响应数据
    result_files = []
    for f in files:
        # 确定文件夹路径
        folder_path = ""
        if f.folder:
            folder_path = f.folder.path

        # 构建URL
        static_dir = "templates/static/uploads"
        file_path = os.path.join(static_dir, folder_path, f.filename) if folder_path else os.path.join(static_dir, f.filename)
        url = f"/static/uploads/{folder_path}/{f.filename}" if folder_path else f"/static/uploads/{f.filename}"

        # 如果文件不存在于static目录，尝试其他位置
        if not os.path.exists(file_path):
            # 尝试其他可能的路径
            alt_paths = [
                f"/static/uploads/{f.filename}",
                f"/{f.filename}",
            ]
            for alt_url in alt_paths:
                alt_path = alt_url.lstrip("/")
                if os.path.exists(alt_path):
                    url = alt_url
                    break

        result_files.append({
            "id": f.id,
            "filename": f.filename,
            "original_name": f.original_name or f.filename,
            "type": f.type,
            "mime_type": f.mime_type,
            "size": f.size,
            "url": url,
            "folder": folder_path,
            "created_at": f.created_at.isoformat() if f.created_at else None,
        })

    return JSONResponse(content={
        "success": True,
        "files": result_files,
        "total": total,
        "limit": limit,
        "offset": offset,
        "folders": [{"id": fo.id, "name": fo.name, "path": fo.path} for fo in folders]
    })


# ============================================================
# 统计 API
# ============================================================


@router.get("/api/stats")
async def get_media_stats(db: Session = Depends(get_db)):
    """获取媒体库统计信息 API"""
    # 总文件数
    total_files = db.query(MediaFile).count()

    # 图片统计
    total_images = db.query(MediaFile).filter(MediaFile.file_type == 'image').count()
    image_size = db.query(func.sum(MediaFile.size)).filter(MediaFile.file_type == 'image').scalar() or 0

    # 视频统计
    total_videos = db.query(MediaFile).filter(MediaFile.file_type == 'video').count()
    video_size = db.query(func.sum(MediaFile.size)).filter(MediaFile.file_type == 'video').scalar() or 0

    # 文档统计
    total_documents = db.query(MediaFile).filter(MediaFile.file_type == 'document').count()
    doc_size = db.query(func.sum(MediaFile.size)).filter(MediaFile.file_type == 'document').scalar() or 0

    # 总大小
    total_size = db.query(func.sum(MediaFile.size)).scalar() or 0

    return JSONResponse(content={
        "success": True,
        "stats": {
            "total_files": total_files,
            "total_images": total_images,
            "total_videos": total_videos,
            "total_documents": total_documents,
            "total_size": total_size,
            "image_size": image_size,
            "video_size": video_size,
            "document_size": doc_size,
        }
    })


@router.get("/api/recent")
async def get_recent_uploads(
    limit: int = 5,
    db: Session = Depends(get_db),
):
    """获取最近上传的文件 API"""
    files = (
        db.query(MediaFile)
        .order_by(MediaFile.created_at.desc())
        .limit(limit)
        .all()
    )

    result_files = []
    for f in files:
        result_files.append({
            "id": f.id,
            "filename": f.filename_original or f.filename,
            "filename_original": f.filename_original or f.filename,
            "path_thumb": f.path_thumb,
            "path_original": f.path_original,
            "file_type": f.file_type,
            "created_at": f.created_at.isoformat() if f.created_at else None,
        })

    return JSONResponse(content={
        "success": True,
        "files": result_files
    })
