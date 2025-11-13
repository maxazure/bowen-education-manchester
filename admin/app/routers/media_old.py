"""
媒体库管理路由

提供媒体文件的上传、查询、更新、删除功能
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from PIL import Image
from pydantic import BaseModel
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models.media import MediaFile

router = APIRouter()

# 配置常量
UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
IMAGES_DIR = UPLOAD_DIR / "images"
THUMBNAILS_DIR = UPLOAD_DIR / "thumbnails"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
THUMBNAIL_SIZE = (300, 300)
ALLOWED_MIME_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
}


class MediaUpdateRequest(BaseModel):
    """媒体更新请求"""

    title: Optional[str] = None
    alt_text: Optional[str] = None
    caption: Optional[str] = None


class MediaListResponse(BaseModel):
    """媒体列表响应"""

    items: list
    total: int
    page: int
    per_page: int


def sanitize_filename(filename: str) -> str:
    """
    清洗文件名，移除特殊字符

    Args:
        filename: 原始文件名

    Returns:
        str: 清洗后的安全文件名
    """
    # 移除路径遍历字符
    filename = os.path.basename(filename)

    # 移除特殊字符，只保留字母、数字、下划线、连字符和点
    filename = re.sub(r"[^\w\-.]", "_", filename)

    # 确保不以点开头（隐藏文件）
    if filename.startswith("."):
        filename = "_" + filename[1:]

    return filename


def generate_unique_filename(filename: str, directory: Path) -> str:
    """
    生成唯一文件名（处理重复）

    Args:
        filename: 原始文件名
        directory: 保存目录

    Returns:
        str: 唯一文件名
    """
    base_name, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename

    while (directory / unique_filename).exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{base_name}_{timestamp}_{counter}{ext}"
        counter += 1

    return unique_filename


def create_thumbnail(
    image_path: Path, thumbnail_path: Path, size: tuple = THUMBNAIL_SIZE
):
    """
    生成缩略图

    Args:
        image_path: 原图路径
        thumbnail_path: 缩略图保存路径
        size: 缩略图尺寸 (width, height)
    """
    with Image.open(image_path) as img:
        # 保持比例缩放
        img.thumbnail(size, Image.Resampling.LANCZOS)

        # 保存缩略图
        img.save(thumbnail_path, quality=90, optimize=True)


@router.post("/upload", status_code=201)
async def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    上传媒体文件

    Args:
        file: 上传的文件
        db: 数据库会话

    Returns:
        dict: 媒体信息

    Raises:
        HTTPException: 文件类型不支持或文件过大
    """
    # 验证文件类型
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型: {file.content_type}。支持的类型: {', '.join(ALLOWED_MIME_TYPES.keys())}",
        )

    # 读取文件内容
    contents = await file.read()
    file_size = len(contents)

    # 验证文件大小
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制。最大允许: {MAX_FILE_SIZE / (1024 * 1024):.1f}MB",
        )

    # 清洗文件名
    safe_filename = sanitize_filename(file.filename)

    # 生成唯一文件名
    unique_filename = generate_unique_filename(safe_filename, IMAGES_DIR)

    # 保存原图
    original_path = IMAGES_DIR / unique_filename
    with open(original_path, "wb") as f:
        f.write(contents)

    # 获取图片尺寸
    try:
        with Image.open(original_path) as img:
            width, height = img.size
    except Exception:
        width = None
        height = None

    # 生成缩略图
    thumbnail_filename = f"thumb_{unique_filename}"
    thumbnail_path = THUMBNAILS_DIR / thumbnail_filename

    try:
        create_thumbnail(original_path, thumbnail_path)
    except Exception as e:
        # 缩略图生成失败不应该阻止上传
        thumbnail_path = None
        print(f"缩略图生成失败: {e}")

    # 创建数据库记录
    media = MediaFile(
        filename_original=safe_filename,
        mime_type=file.content_type,
        size_bytes=file_size,
        width=width,
        height=height,
        path_original=str(original_path),
        path_thumb=str(thumbnail_path) if thumbnail_path else None,
        usage_count=0,
    )

    db.add(media)
    db.commit()
    db.refresh(media)

    # 返回响应
    return {
        "id": media.id,
        "filename_original": media.filename_original,
        "mime_type": media.mime_type,
        "size_bytes": media.size_bytes,
        "width": media.width,
        "height": media.height,
        "path_original": media.path_original,
        "path_thumb": media.path_thumb,
        "usage_count": media.usage_count,
        "created_at": media.created_at.isoformat() if media.created_at else None,
        "updated_at": media.updated_at.isoformat() if media.updated_at else None,
    }


@router.get("", response_model=MediaListResponse)
async def get_media_list(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    mime_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    获取媒体列表（支持分页、搜索、筛选）

    Args:
        page: 页码（从 1 开始）
        per_page: 每页数量
        search: 搜索关键词（文件名）
        mime_type: MIME 类型筛选
        db: 数据库会话

    Returns:
        MediaListResponse: 媒体列表和分页信息
    """
    query = db.query(MediaFile)

    # 搜索
    if search:
        query = query.filter(MediaFile.filename_original.contains(search))

    # 类型筛选
    if mime_type:
        query = query.filter(MediaFile.mime_type == mime_type)

    # 总数
    total = query.count()

    # 分页
    offset = (page - 1) * per_page
    items = (
        query.order_by(MediaFile.created_at.desc()).offset(offset).limit(per_page).all()
    )

    # 格式化返回数据
    items_data = [
        {
            "id": item.id,
            "filename_original": item.filename_original,
            "mime_type": item.mime_type,
            "size_bytes": item.size_bytes,
            "width": item.width,
            "height": item.height,
            "path_original": item.path_original,
            "path_thumb": item.path_thumb,
            "usage_count": item.usage_count,
            "title": item.title,
            "alt_text": item.alt_text,
            "caption": item.caption,
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "updated_at": item.updated_at.isoformat() if item.updated_at else None,
        }
        for item in items
    ]

    return {
        "items": items_data,
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/{media_id}")
async def get_media_detail(media_id: int, db: Session = Depends(get_db)):
    """
    获取单个媒体详情

    Args:
        media_id: 媒体 ID
        db: 数据库会话

    Returns:
        dict: 媒体详情

    Raises:
        HTTPException: 媒体不存在
    """
    media = db.query(MediaFile).filter(MediaFile.id == media_id).first()

    if not media:
        raise HTTPException(status_code=404, detail="媒体不存在")

    return {
        "id": media.id,
        "filename_original": media.filename_original,
        "mime_type": media.mime_type,
        "size_bytes": media.size_bytes,
        "width": media.width,
        "height": media.height,
        "path_original": media.path_original,
        "path_thumb": media.path_thumb,
        "usage_count": media.usage_count,
        "title": media.title,
        "alt_text": media.alt_text,
        "caption": media.caption,
        "created_at": media.created_at.isoformat() if media.created_at else None,
        "updated_at": media.updated_at.isoformat() if media.updated_at else None,
    }


@router.put("/{media_id}")
async def update_media(
    media_id: int,
    data: MediaUpdateRequest,
    db: Session = Depends(get_db),
):
    """
    更新媒体元数据

    Args:
        media_id: 媒体 ID
        data: 更新数据
        db: 数据库会话

    Returns:
        dict: 更新后的媒体信息

    Raises:
        HTTPException: 媒体不存在
    """
    media = db.query(MediaFile).filter(MediaFile.id == media_id).first()

    if not media:
        raise HTTPException(status_code=404, detail="媒体不存在")

    # 更新字段
    if data.title is not None:
        media.title = data.title
    if data.alt_text is not None:
        media.alt_text = data.alt_text
    if data.caption is not None:
        media.caption = data.caption

    db.commit()
    db.refresh(media)

    return {
        "id": media.id,
        "filename_original": media.filename_original,
        "mime_type": media.mime_type,
        "size_bytes": media.size_bytes,
        "width": media.width,
        "height": media.height,
        "path_original": media.path_original,
        "path_thumb": media.path_thumb,
        "usage_count": media.usage_count,
        "title": media.title,
        "alt_text": media.alt_text,
        "caption": media.caption,
        "created_at": media.created_at.isoformat() if media.created_at else None,
        "updated_at": media.updated_at.isoformat() if media.updated_at else None,
    }


@router.delete("/{media_id}", status_code=204)
async def delete_media(media_id: int, db: Session = Depends(get_db)):
    """
    删除媒体（带删除保护）

    Args:
        media_id: 媒体 ID
        db: 数据库会话

    Raises:
        HTTPException: 媒体不存在或正在被使用
    """
    media = db.query(MediaFile).filter(MediaFile.id == media_id).first()

    if not media:
        raise HTTPException(status_code=404, detail="媒体不存在")

    # 删除保护：检查使用次数
    if media.usage_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"媒体正在被使用（{media.usage_count} 次引用），无法删除",
        )

    # 删除文件
    try:
        # 删除原图
        if media.path_original and Path(media.path_original).exists():
            Path(media.path_original).unlink()

        # 删除缩略图
        if media.path_thumb and Path(media.path_thumb).exists():
            Path(media.path_thumb).unlink()
    except Exception as e:
        print(f"删除文件失败: {e}")

    # 删除数据库记录
    db.delete(media)
    db.commit()

    return None
