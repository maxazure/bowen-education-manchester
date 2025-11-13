"""
相册管理路由

提供相册的 CRUD 操作、图片管理、排序等功能
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from slugify import slugify
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.gallery import Gallery, GalleryImage
from app.models.media import MediaFile

router = APIRouter(prefix="/galleries", tags=["galleries"])


# ===== Schemas =====


class GalleryCreate(BaseModel):
    """创建相册的请求模型"""

    title: str = Field(..., min_length=1, max_length=200, description="相册标题")
    description: Optional[str] = Field(None, description="相册描述")
    category: Optional[str] = Field(None, max_length=100, description="分类")
    tags: Optional[str] = Field(None, max_length=255, description="标签（逗号分隔）")
    cover_media_id: Optional[int] = Field(None, description="封面图ID")
    display_mode: str = Field("grid", description="展示模式: grid, masonry, carousel")
    is_featured: bool = Field(False, description="是否推荐")
    is_public: bool = Field(True, description="是否公开")
    allow_download: bool = Field(False, description="允许下载")
    watermark_enabled: bool = Field(False, description="启用水印")


class GalleryUpdate(BaseModel):
    """更新相册的请求模型"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = Field(None, max_length=255)
    cover_media_id: Optional[int] = None
    display_mode: Optional[str] = None
    is_featured: Optional[bool] = None
    is_public: Optional[bool] = None
    allow_download: Optional[bool] = None
    watermark_enabled: Optional[bool] = None


class GalleryImageData(BaseModel):
    """相册图片数据"""

    media_id: int = Field(..., description="媒体文件ID")
    title: Optional[str] = Field(None, max_length=200, description="图片标题")
    caption: Optional[str] = Field(None, description="图片说明")
    sort_order: int = Field(0, description="排序序号")


class BatchAddImagesRequest(BaseModel):
    """批量添加图片请求"""

    images: List[GalleryImageData] = Field(..., description="图片列表")


class GalleryImageUpdate(BaseModel):
    """更新图片元数据"""

    title: Optional[str] = Field(None, max_length=200)
    caption: Optional[str] = None
    alt_text: Optional[str] = Field(None, max_length=255)


class DragSortRequest(BaseModel):
    """拖拽排序请求"""

    image_id: int = Field(..., description="要移动的图片ID")
    new_position: int = Field(..., ge=0, description="新位置（从0开始）")


class BatchReorderRequest(BaseModel):
    """批量重排序请求"""

    order: List[dict] = Field(
        ..., description="新的排序列表，每项包含 id 和 sort_order"
    )


class SetCoverRequest(BaseModel):
    """设置封面图请求"""

    media_id: int = Field(..., description="媒体文件ID")


class GalleryResponse(BaseModel):
    """相册响应模型"""

    id: int
    title: str
    slug: str
    description: Optional[str]
    category: Optional[str]
    tags: Optional[str]
    cover_media_id: Optional[int]
    display_mode: str
    is_featured: bool
    is_public: bool
    allow_download: bool
    watermark_enabled: bool
    image_count: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        json_encoders = {"datetime": lambda v: v.isoformat() if v else None}


class GalleryImageResponse(BaseModel):
    """图片响应模型"""

    id: int
    gallery_id: int
    media_id: int
    title: Optional[str]
    caption: Optional[str]
    alt_text: Optional[str]
    sort_order: int
    is_visible: bool
    is_featured: bool

    class Config:
        from_attributes = True


# ===== Routes =====


@router.post("", status_code=status.HTTP_200_OK)
def create_gallery(
    gallery_data: GalleryCreate,
    db: Session = Depends(get_db),
) -> dict:
    """
    创建新相册

    Args:
        gallery_data: 相册数据
        db: 数据库会话

    Returns:
        创建的相册对象
    """
    # 生成 slug
    slug = slugify(gallery_data.title)

    # 检查 slug 是否重复
    existing = db.query(Gallery).filter_by(slug=slug).first()
    if existing:
        # 添加数字后缀
        counter = 1
        while db.query(Gallery).filter_by(slug=f"{slug}-{counter}").first():
            counter += 1
        slug = f"{slug}-{counter}"

    # 创建相册
    gallery = Gallery(
        title=gallery_data.title,
        slug=slug,
        description=gallery_data.description,
        category=gallery_data.category,
        tags=gallery_data.tags,
        cover_media_id=gallery_data.cover_media_id,
        display_mode=gallery_data.display_mode,
        is_featured=gallery_data.is_featured,
        is_public=gallery_data.is_public,
        allow_download=gallery_data.allow_download,
        watermark_enabled=gallery_data.watermark_enabled,
    )

    db.add(gallery)
    db.commit()
    db.refresh(gallery)

    # 转换为字典返回
    return {
        "id": gallery.id,
        "title": gallery.title,
        "slug": gallery.slug,
        "description": gallery.description,
        "category": gallery.category,
        "tags": gallery.tags,
        "cover_media_id": gallery.cover_media_id,
        "display_mode": gallery.display_mode,
        "is_featured": gallery.is_featured,
        "is_public": gallery.is_public,
        "allow_download": gallery.allow_download,
        "watermark_enabled": gallery.watermark_enabled,
        "image_count": gallery.image_count,
        "created_at": gallery.created_at.isoformat() if gallery.created_at else None,
        "updated_at": gallery.updated_at.isoformat() if gallery.updated_at else None,
    }


@router.put("/{gallery_id}")
def update_gallery(
    gallery_id: int,
    gallery_data: GalleryUpdate,
    db: Session = Depends(get_db),
) -> dict:
    """
    更新相册

    Args:
        gallery_id: 相册ID
        gallery_data: 更新数据
        db: 数据库会话

    Returns:
        更新后的相册对象
    """
    gallery = db.query(Gallery).filter_by(id=gallery_id).first()
    if not gallery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gallery with id {gallery_id} not found",
        )

    # 更新字段
    update_dict = gallery_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(gallery, key, value)

    db.commit()
    db.refresh(gallery)

    return {
        "id": gallery.id,
        "title": gallery.title,
        "slug": gallery.slug,
        "description": gallery.description,
        "category": gallery.category,
        "tags": gallery.tags,
        "cover_media_id": gallery.cover_media_id,
        "display_mode": gallery.display_mode,
        "is_featured": gallery.is_featured,
        "is_public": gallery.is_public,
        "allow_download": gallery.allow_download,
        "watermark_enabled": gallery.watermark_enabled,
        "image_count": gallery.image_count,
        "created_at": gallery.created_at.isoformat() if gallery.created_at else None,
        "updated_at": gallery.updated_at.isoformat() if gallery.updated_at else None,
    }


@router.delete("/{gallery_id}")
def delete_gallery(
    gallery_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """
    删除相册

    Args:
        gallery_id: 相册ID
        db: 数据库会话

    Returns:
        删除结果
    """
    gallery = db.query(Gallery).filter_by(id=gallery_id).first()
    if not gallery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gallery with id {gallery_id} not found",
        )

    db.delete(gallery)
    db.commit()

    return {"success": True, "message": f"Gallery {gallery_id} deleted"}


@router.post("/{gallery_id}/images/batch")
def batch_add_images(
    gallery_id: int,
    request: BatchAddImagesRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    批量添加图片到相册

    Args:
        gallery_id: 相册ID
        request: 批量添加请求
        db: 数据库会话

    Returns:
        添加结果
    """
    # 验证相册存在
    gallery = db.query(Gallery).filter_by(id=gallery_id).first()
    if not gallery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gallery with id {gallery_id} not found",
        )

    # 批量添加图片
    added_count = 0
    for img_data in request.images:
        # 验证媒体文件存在
        media = db.query(MediaFile).filter_by(id=img_data.media_id).first()
        if not media:
            continue

        gallery_image = GalleryImage(
            gallery_id=gallery_id,
            media_id=img_data.media_id,
            title=img_data.title,
            caption=img_data.caption,
            sort_order=img_data.sort_order,
        )
        db.add(gallery_image)
        added_count += 1

    db.commit()

    # 更新相册的图片计数
    gallery.image_count = (
        db.query(GalleryImage).filter_by(gallery_id=gallery_id).count()
    )
    db.commit()

    return {"success": True, "added_count": added_count}


@router.patch("/{gallery_id}/images/{image_id}", response_model=GalleryImageResponse)
def update_image_metadata(
    gallery_id: int,
    image_id: int,
    update_data: GalleryImageUpdate,
    db: Session = Depends(get_db),
) -> GalleryImage:
    """
    更新图片元数据

    Args:
        gallery_id: 相册ID
        image_id: 图片ID
        update_data: 更新数据
        db: 数据库会话

    Returns:
        更新后的图片对象
    """
    image = db.query(GalleryImage).filter_by(id=image_id, gallery_id=gallery_id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id {image_id} not found in gallery {gallery_id}",
        )

    # 更新字段
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(image, key, value)

    db.commit()
    db.refresh(image)

    return image


@router.post("/{gallery_id}/images/{image_id}/toggle-visibility")
def toggle_image_visibility(
    gallery_id: int,
    image_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """
    切换图片的显示/隐藏状态

    Args:
        gallery_id: 相册ID
        image_id: 图片ID
        db: 数据库会话

    Returns:
        新的显示状态
    """
    image = db.query(GalleryImage).filter_by(id=image_id, gallery_id=gallery_id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id {image_id} not found in gallery {gallery_id}",
        )

    # 切换状态
    image.is_visible = not image.is_visible
    db.commit()
    db.refresh(image)

    return {"id": image.id, "is_visible": image.is_visible}


@router.post("/{gallery_id}/set-cover")
def set_cover_image(
    gallery_id: int,
    request: SetCoverRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    设置相册封面图

    Args:
        gallery_id: 相册ID
        request: 设置封面请求
        db: 数据库会话

    Returns:
        更新后的相册对象
    """
    gallery = db.query(Gallery).filter_by(id=gallery_id).first()
    if not gallery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gallery with id {gallery_id} not found",
        )

    # 验证媒体文件存在
    media = db.query(MediaFile).filter_by(id=request.media_id).first()
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media file with id {request.media_id} not found",
        )

    # 设置封面
    gallery.cover_media_id = request.media_id
    db.commit()
    db.refresh(gallery)

    return {
        "id": gallery.id,
        "title": gallery.title,
        "slug": gallery.slug,
        "description": gallery.description,
        "category": gallery.category,
        "tags": gallery.tags,
        "cover_media_id": gallery.cover_media_id,
        "display_mode": gallery.display_mode,
        "is_featured": gallery.is_featured,
        "is_public": gallery.is_public,
        "allow_download": gallery.allow_download,
        "watermark_enabled": gallery.watermark_enabled,
        "image_count": gallery.image_count,
        "created_at": gallery.created_at.isoformat() if gallery.created_at else None,
        "updated_at": gallery.updated_at.isoformat() if gallery.updated_at else None,
    }


@router.post("/{gallery_id}/images/drag-sort")
def drag_sort_images(
    gallery_id: int,
    request: DragSortRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    拖拽排序图片

    Args:
        gallery_id: 相册ID
        request: 拖拽排序请求
        db: 数据库会话

    Returns:
        排序结果
    """
    # 获取相册所有图片
    images = (
        db.query(GalleryImage)
        .filter_by(gallery_id=gallery_id)
        .order_by(GalleryImage.sort_order)
        .all()
    )

    if not images:
        return {"success": True, "message": "No images to sort"}

    # 找到要移动的图片
    moving_image = None
    old_position = None
    for i, img in enumerate(images):
        if img.id == request.image_id:
            moving_image = img
            old_position = i
            break

    if moving_image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id {request.image_id} not found",
        )

    # 如果位置没变，直接返回
    if old_position == request.new_position:
        return {"success": True, "message": "Position unchanged"}

    # 移除图片
    images.pop(old_position)

    # 插入到新位置
    images.insert(request.new_position, moving_image)

    # 更新所有图片的 sort_order
    for i, img in enumerate(images):
        img.sort_order = i

    db.commit()

    return {"success": True, "message": "Images reordered successfully"}


@router.post("/{gallery_id}/images/reorder")
def batch_reorder_images(
    gallery_id: int,
    request: BatchReorderRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    批量更新图片排序

    Args:
        gallery_id: 相册ID
        request: 批量重排序请求
        db: 数据库会话

    Returns:
        更新结果
    """
    # 验证相册存在
    gallery = db.query(Gallery).filter_by(id=gallery_id).first()
    if not gallery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gallery with id {gallery_id} not found",
        )

    # 更新每张图片的 sort_order
    updated_count = 0
    for item in request.order:
        image_id = item.get("id")
        new_sort_order = item.get("sort_order")

        if image_id is None or new_sort_order is None:
            continue

        image = (
            db.query(GalleryImage).filter_by(id=image_id, gallery_id=gallery_id).first()
        )

        if image:
            image.sort_order = new_sort_order
            updated_count += 1

    db.commit()

    return {"success": True, "updated_count": updated_count}
