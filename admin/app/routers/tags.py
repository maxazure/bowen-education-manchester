"""
标签管理路由

管理后台内容标签的CRUD操作
"""

import re
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from admin.app.database import get_db
from admin.app.dependencies import get_current_admin_user
from app.models import AdminUser
from app.models.tag import Tag, PostTagLink

router = APIRouter(tags=["tags"])

templates = Jinja2Templates(directory="admin/templates")


def slugify(text: str) -> str:
    """将文本转换为URL友好的slug"""
    # 转换为小写
    slug = text.lower()
    # 替换空格和下划线为连字符
    slug = re.sub(r'[\s_]+', '-', slug)
    # 移除非字母数字和连字符的字符
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # 移除连续连字符
    slug = re.sub(r'-+', '-', slug)
    # 移除首尾连字符
    slug = slug.strip('-')
    return slug


@router.get("/tags", response_class=HTMLResponse)
async def tags_list(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """标签管理列表页"""
    # 获取所有标签
    tags = db.query(Tag).order_by(Tag.sort_order, Tag.name).all()

    # 计算统计数据
    total_tags = len(tags)
    active_tags = len([t for t in tags if t.is_active])
    total_posts = db.query(PostTagLink).count()

    return templates.TemplateResponse(
        "tags/list.html",
        {
            "request": request,
            "tags": tags,
            "total_tags": total_tags,
            "active_tags": active_tags,
            "total_posts": total_posts,
        },
    )


@router.get("/tags/new", response_class=HTMLResponse)
async def new_tag_form(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """新建标签表单"""
    return templates.TemplateResponse(
        "tags/form.html",
        {
            "request": request,
            "tag": None,
            "action": "/admin/tags",
            "method": "POST",
        },
    )


@router.post("/tags", response_class=JSONResponse)
async def create_tag(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """创建标签"""
    try:
        data = await request.json()

        name = data.get("name", "").strip()
        name_en = data.get("name_en", "").strip() or None
        description = data.get("description", "").strip() or None
        description_en = data.get("description_en", "").strip() or None
        color = data.get("color", "#667eea").strip()
        icon = data.get("icon", "").strip() or None

        if not name:
            return JSONResponse(
                content={"success": False, "message": "请输入标签名称"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 生成slug
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while db.query(Tag).filter(Tag.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        tag = Tag(
            name=name,
            name_en=name_en,
            slug=slug,
            color=color,
            description=description,
            description_en=description_en,
            icon=icon,
            is_active=True,
            sort_order=data.get("sort_order", 0) or 0,
        )

        db.add(tag)
        db.commit()
        db.refresh(tag)

        return JSONResponse(
            content={"success": True, "message": "标签创建成功", "tag_id": tag.id},
            status_code=status.HTTP_201_CREATED,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"创建失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/tags/{tag_id}/edit", response_class=HTMLResponse)
async def edit_tag_form(
    request: Request,
    tag_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """编辑标签表单"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")

    return templates.TemplateResponse(
        "tags/form.html",
        {
            "request": request,
            "tag": tag,
            "action": f"/admin/tags/{tag_id}",
            "method": "POST",
        },
    )


@router.post("/tags/{tag_id}", response_class=JSONResponse)
async def update_tag(
    request: Request,
    tag_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """更新标签"""
    try:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()

        if not tag:
            return JSONResponse(
                content={"success": False, "message": "标签不存在"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        data = await request.json()

        tag.name = data.get("name", tag.name).strip()
        tag.name_en = data.get("name_en", "") or None
        if tag.name_en == "":
            tag.name_en = None

        tag.description = data.get("description", "") or None
        if tag.description == "":
            tag.description = None

        tag.description_en = data.get("description_en", "") or None
        if tag.description_en == "":
            tag.description_en = None

        tag.color = data.get("color", tag.color).strip()
        tag.icon = data.get("icon", "") or None
        if tag.icon == "":
            tag.icon = None

        tag.is_active = data.get("is_active", tag.is_active)
        tag.sort_order = data.get("sort_order", tag.sort_order) or 0
        tag.updated_at = datetime.now()

        db.commit()

        return JSONResponse(
            content={"success": True, "message": "标签更新成功"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"更新失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.delete("/tags/{tag_id}", response_class=JSONResponse)
async def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """删除标签"""
    try:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()

        if not tag:
            return JSONResponse(
                content={"success": False, "message": "标签不存在"},
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # 删除关联记录
        db.query(PostTagLink).filter(PostTagLink.tag_id == tag_id).delete()

        # 删除标签
        db.delete(tag)
        db.commit()

        return JSONResponse(
            content={"success": True, "message": "标签删除成功"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/api/tags", response_class=JSONResponse)
async def get_tags_api(
    active_only: bool = True,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取标签列表API"""
    query = db.query(Tag)

    if active_only:
        query = query.filter(Tag.is_active == True)

    tags = query.order_by(Tag.sort_order, Tag.name).all()

    return JSONResponse(
        content={
            "success": True,
            "data": [
                {
                    "id": tag.id,
                    "name": tag.name,
                    "name_en": tag.name_en,
                    "slug": tag.slug,
                    "color": tag.color,
                    "icon": tag.icon,
                }
                for tag in tags
            ],
        }
    )


@router.get("/api/tags/{tag_id}", response_class=JSONResponse)
async def get_tag_api(
    tag_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取单个标签API"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        return JSONResponse(
            content={"success": False, "message": "标签不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # 获取使用此标签的文章
    posts = db.query(PostTagLink).filter(PostTagLink.tag_id == tag_id).count()

    return JSONResponse(
        content={
            "success": True,
            "data": {
                "id": tag.id,
                "name": tag.name,
                "name_en": tag.name_en,
                "slug": tag.slug,
                "color": tag.color,
                "description": tag.description,
                "description_en": tag.description_en,
                "icon": tag.icon,
                "is_active": tag.is_active,
                "sort_order": tag.sort_order,
                "post_count": posts,
                "created_at": tag.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": tag.updated_at.strftime("%Y-%m-%d %H:%M:%S") if tag.updated_at else None,
            },
        }
    )


@router.post("/tags/{tag_id}/toggle", response_class=JSONResponse)
async def toggle_tag_status(
    tag_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """切换标签启用状态"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        return JSONResponse(
            content={"success": False, "message": "标签不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    tag.is_active = not tag.is_active
    tag.updated_at = datetime.now()
    db.commit()

    status_text = "启用" if tag.is_active else "禁用"
    return JSONResponse(
        content={"success": True, "message": f"标签已{status_text}"},
        status_code=status.HTTP_200_OK,
    )


@router.post("/tags/reorder", response_class=JSONResponse)
async def reorder_tags(
    request: Request,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """批量调整标签排序"""
    try:
        data = await request.json()
        tag_orders = data.get("tag_orders", [])

        for item in tag_orders:
            tag_id = item.get("id")
            sort_order = item.get("sort_order", 0)

            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                tag.sort_order = sort_order

        db.commit()

        return JSONResponse(
            content={"success": True, "message": "排序更新成功"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"排序更新失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


# ========== 文章标签关联管理 ==========

@router.get("/api/posts/{post_id}/tags", response_class=JSONResponse)
async def get_post_tags(
    post_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """获取文章的标签"""
    from app.models.post import Post

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    tags = [
        {
            "id": tag.id,
            "name": tag.name,
            "name_en": tag.name_en,
            "slug": tag.slug,
            "color": tag.color,
        }
        for tag in post.tags
    ]

    return JSONResponse(
        content={"success": True, "data": tags}
    )


@router.post("/api/posts/{post_id}/tags", response_class=JSONResponse)
async def update_post_tags(
    request: Request,
    post_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin_user),
):
    """更新文章的标签"""
    from app.models.post import Post

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return JSONResponse(
            content={"success": False, "message": "文章不存在"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    try:
        data = await request.json()
        tag_ids = data.get("tag_ids", [])

        # 清除现有标签关联
        db.query(PostTagLink).filter(PostTagLink.post_id == post_id).delete()

        # 添加新的标签关联
        for tag_id in tag_ids:
            # 验证标签存在
            tag = db.query(Tag).filter(Tag.id == tag_id, Tag.is_active == True).first()
            if tag:
                link = PostTagLink(post_id=post_id, tag_id=tag_id)
                db.add(link)

        db.commit()

        return JSONResponse(
            content={"success": True, "message": "标签更新成功"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"更新失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
