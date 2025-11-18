"""
栏目管理路由

提供栏目的 CRUD 操作和树形结构展示
"""

from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models.site import ColumnType, SiteColumn
from app.services import column_service
from admin.app.routers.static_pages import generate_static_task

router = APIRouter(prefix="/columns", tags=["columns"])
templates = Jinja2Templates(directory="admin/templates")


@router.get("", response_class=HTMLResponse)
async def list_columns(request: Request, db: Session = Depends(get_db)):
    """
    栏目列表页面

    显示树形结构的栏目列表，支持拖拽排序

    Args:
        request: FastAPI request 对象
        db: 数据库会话

    Returns:
        栏目列表页面 HTML
    """
    # 构建树形结构
    tree = column_service.build_tree(db)

    # 获取所有栏目（用于编辑时选择父栏目）
    all_columns = column_service.get_all_columns(db)

    return templates.TemplateResponse(
        "columns/list.html",
        {
            "request": request,
            "tree": tree,
            "all_columns": all_columns,
            "column_types": ColumnType,
        },
    )


@router.get("/new", response_class=HTMLResponse)
async def new_column_page(request: Request, db: Session = Depends(get_db)):
    """
    新建栏目页面

    Args:
        request: FastAPI request 对象
        db: 数据库会话

    Returns:
        新建栏目表单页面 HTML
    """
    # 获取所有栏目（用于选择父栏目）
    all_columns = column_service.get_all_columns(db, enabled_only=True)

    return templates.TemplateResponse(
        "columns/form.html",
        {
            "request": request,
            "column": None,
            "all_columns": all_columns,
            "column_types": ColumnType,
            "mode": "create",
        },
    )


@router.post("")
async def create_column(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    slug: Optional[str] = Form(None),
    column_type: str = Form(...),
    description: Optional[str] = Form(None),
    parent_id: Optional[int] = Form(None),
    sort_order: int = Form(0),
    menu_location: str = Form("header"),
    show_in_nav: bool = Form(True),
    is_enabled: bool = Form(True),
    icon: Optional[str] = Form(None),
    hero_title: Optional[str] = Form(None),
    hero_title_en: Optional[str] = Form(None),
    hero_tagline: Optional[str] = Form(None),
    hero_tagline_en: Optional[str] = Form(None),
    hero_cta_text: Optional[str] = Form(None),
    hero_cta_url: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """
    创建栏目

    Args:
        request: FastAPI request 对象
        name: 栏目名称
        slug: URL slug（可选，自动生成）
        column_type: 栏目类型
        description: 栏目描述
        parent_id: 父栏目 ID
        sort_order: 排序值
        menu_location: 菜单位置
        show_in_nav: 是否显示在导航
        is_enabled: 是否启用
        icon: 图标
        hero_title: Hero 标题
        hero_title_en: Hero 英文标题
        hero_tagline: Hero 标语
        hero_tagline_en: Hero 英文标语
        hero_cta_text: CTA 按钮文本
        hero_cta_url: CTA 按钮链接
        db: 数据库会话

    Returns:
        重定向到栏目列表页面
    """
    # 自动生成 slug（如果未提供）
    if not slug or slug.strip() == "":
        slug = column_service.generate_slug(name, db)

    # 创建栏目对象
    column = SiteColumn(
        name=name,
        slug=slug,
        column_type=ColumnType(column_type),
        description=description,
        parent_id=parent_id if parent_id else None,
        sort_order=sort_order,
        menu_location=menu_location,
        show_in_nav=show_in_nav,
        is_enabled=is_enabled,
        icon=icon,
        hero_title=hero_title,
        hero_title_en=hero_title_en,
        hero_tagline=hero_tagline,
        hero_tagline_en=hero_tagline_en,
        hero_cta_text=hero_cta_text,
        hero_cta_url=hero_cta_url,
    )

    # 保存到数据库
    db.add(column)
    db.commit()
    db.refresh(column)

    # 触发静态页面生成
    background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

    # 重定向到列表页
    return RedirectResponse(url="/admin/columns", status_code=303)


@router.get("/{column_id}/edit", response_class=HTMLResponse)
async def edit_column_page(
    request: Request, column_id: int, db: Session = Depends(get_db)
):
    """
    编辑栏目页面

    Args:
        request: FastAPI request 对象
        column_id: 栏目 ID
        db: 数据库会话

    Returns:
        编辑栏目表单页面 HTML
    """
    # 获取栏目
    column = db.query(SiteColumn).filter_by(id=column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="栏目不存在")

    # 获取所有栏目（用于选择父栏目，但排除自己和自己的子栏目）
    all_columns = column_service.get_all_columns(db, enabled_only=True)

    return templates.TemplateResponse(
        "columns/form.html",
        {
            "request": request,
            "column": column,
            "all_columns": all_columns,
            "column_types": ColumnType,
            "mode": "edit",
        },
    )


@router.post("/{column_id}")
async def update_column(
    request: Request,
    column_id: int,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    slug: str = Form(...),
    column_type: str = Form(...),
    description: Optional[str] = Form(None),
    parent_id: Optional[int] = Form(None),
    sort_order: int = Form(0),
    menu_location: str = Form("header"),
    show_in_nav: bool = Form(True),
    is_enabled: bool = Form(True),
    icon: Optional[str] = Form(None),
    hero_title: Optional[str] = Form(None),
    hero_title_en: Optional[str] = Form(None),
    hero_tagline: Optional[str] = Form(None),
    hero_tagline_en: Optional[str] = Form(None),
    hero_cta_text: Optional[str] = Form(None),
    hero_cta_url: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """
    更新栏目

    Args:
        request: FastAPI request 对象
        column_id: 栏目 ID
        name: 栏目名称
        slug: URL slug
        column_type: 栏目类型
        description: 栏目描述
        parent_id: 父栏目 ID
        sort_order: 排序值
        menu_location: 菜单位置
        show_in_nav: 是否显示在导航
        is_enabled: 是否启用
        icon: 图标
        hero_title: Hero 标题
        hero_title_en: Hero 英文标题
        hero_tagline: Hero 标语
        hero_tagline_en: Hero 英文标语
        hero_cta_text: CTA 按钮文本
        hero_cta_url: CTA 按钮链接
        db: 数据库会话

    Returns:
        重定向到栏目列表页面
    """
    # 获取栏目
    column = db.query(SiteColumn).filter_by(id=column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="栏目不存在")

    # 更新字段
    column.name = name
    column.slug = slug
    column.column_type = ColumnType(column_type)
    column.description = description
    column.parent_id = parent_id if parent_id else None
    column.sort_order = sort_order
    column.menu_location = menu_location
    column.show_in_nav = show_in_nav
    column.is_enabled = is_enabled
    column.icon = icon
    column.hero_title = hero_title
    column.hero_title_en = hero_title_en
    column.hero_tagline = hero_tagline
    column.hero_tagline_en = hero_tagline_en
    column.hero_cta_text = hero_cta_text
    column.hero_cta_url = hero_cta_url

    # 保存到数据库
    db.commit()
    db.refresh(column)

    # 触发静态页面生成
    background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

    # 重定向到列表页
    return RedirectResponse(url="/admin/columns", status_code=303)


@router.delete("/{column_id}")
async def delete_column(column_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    删除栏目

    检查栏目是否包含内容，如果包含则不允许删除

    Args:
        column_id: 栏目 ID
        db: 数据库会话

    Returns:
        JSON 响应
    """
    # 获取栏目
    column = db.query(SiteColumn).filter_by(id=column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="栏目不存在")

    # 检查是否可以删除
    if not column_service.can_delete_column(db, column_id):
        return JSONResponse(
            status_code=400,
            content={
                "error": "该栏目包含子栏目或关联内容，无法删除",
                "message": "请先删除或移动子栏目和关联内容",
            },
        )

    # 删除栏目
    db.delete(column)
    db.commit()

    # 触发静态页面生成
    background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

    return JSONResponse(content={"message": "栏目删除成功", "id": column_id})


@router.post("/reorder")
async def reorder_columns(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    批量更新栏目排序

    接收拖拽后的排序数据并更新数据库

    Args:
        request: FastAPI request 对象
        db: 数据库会话

    Returns:
        JSON 响应

    Request Body Example:
        {
            "order": [
                {"id": 1, "sort_order": 1},
                {"id": 2, "sort_order": 2},
                {"id": 3, "sort_order": 3}
            ]
        }
    """
    # 获取请求体
    data = await request.json()
    order = data.get("order", [])

    if not order:
        return JSONResponse(status_code=400, content={"error": "排序数据不能为空"})

    # 批量更新排序
    for item in order:
        column_id = item.get("id")
        sort_order = item.get("sort_order")

        if column_id is None or sort_order is None:
            continue

        column = db.query(SiteColumn).filter_by(id=column_id).first()
        if column:
            column.sort_order = sort_order

    # 提交事务
    db.commit()

    # 触发静态页面生成
    background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

    return JSONResponse(content={"message": "排序更新成功", "count": len(order)})


@router.post("/{column_id}/toggle")
async def toggle_column_status(column_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    切换栏目启用/禁用状态

    Args:
        column_id: 栏目 ID
        db: 数据库会话

    Returns:
        JSON 响应
    """
    # 获取栏目
    column = db.query(SiteColumn).filter_by(id=column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="栏目不存在")

    # 切换状态
    column.is_enabled = not column.is_enabled
    db.commit()

    # 触发静态页面生成
    background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

    return JSONResponse(
        content={
            "message": "状态更新成功",
            "id": column_id,
            "is_enabled": column.is_enabled,
        }
    )


@router.post("/batch/status")
async def batch_update_status(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    批量更新栏目启用状态

    Args:
        request: FastAPI request 对象
        db: 数据库会话

    Returns:
        JSON 响应

    Request Body:
        {
            "column_ids": [1, 2, 3],
            "is_enabled": true
        }
    """
    data = await request.json()
    column_ids = data.get("column_ids", [])
    is_enabled = data.get("is_enabled", True)

    if not column_ids:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "未选择栏目"}
        )

    # 批量更新
    updated_count = 0
    for column_id in column_ids:
        column = db.query(SiteColumn).filter_by(id=column_id).first()
        if column:
            column.is_enabled = is_enabled
            updated_count += 1

    db.commit()

    # 触发静态页面生成
    background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

    action = "启用" if is_enabled else "禁用"
    return JSONResponse(
        content={
            "success": True,
            "message": f"成功{action} {updated_count} 个栏目",
            "count": updated_count,
        }
    )


@router.post("/batch/nav")
async def batch_update_nav(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    批量更新栏目导航显示状态

    Args:
        request: FastAPI request 对象
        db: 数据库会话

    Returns:
        JSON 响应

    Request Body:
        {
            "column_ids": [1, 2, 3],
            "show_in_nav": true
        }
    """
    data = await request.json()
    column_ids = data.get("column_ids", [])
    show_in_nav = data.get("show_in_nav", True)

    if not column_ids:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "未选择栏目"}
        )

    # 批量更新
    updated_count = 0
    for column_id in column_ids:
        column = db.query(SiteColumn).filter_by(id=column_id).first()
        if column:
            column.show_in_nav = show_in_nav
            updated_count += 1

    db.commit()

    # 触发静态页面生成
    background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

    action = "显示在导航" if show_in_nav else "不显示在导航"
    return JSONResponse(
        content={
            "success": True,
            "message": f"成功将 {updated_count} 个栏目设置为{action}",
            "count": updated_count,
        }
    )


@router.post("/batch/delete")
async def batch_delete_columns(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    批量删除栏目

    Args:
        request: FastAPI request 对象
        db: 数据库会话

    Returns:
        JSON 响应

    Request Body:
        {
            "column_ids": [1, 2, 3]
        }
    """
    data = await request.json()
    column_ids = data.get("column_ids", [])

    if not column_ids:
        return JSONResponse(
            status_code=400, content={"success": False, "message": "未选择栏目"}
        )

    # 批量删除
    deleted_count = 0
    failed_columns = []

    for column_id in column_ids:
        # 检查是否可以删除
        if column_service.can_delete_column(db, column_id):
            column = db.query(SiteColumn).filter_by(id=column_id).first()
            if column:
                db.delete(column)
                deleted_count += 1
        else:
            column = db.query(SiteColumn).filter_by(id=column_id).first()
            if column:
                failed_columns.append(column.name)

    db.commit()

    # 触发静态页面生成
    background_tasks.add_task(generate_static_task, "public", "http://localhost:8000")

    if failed_columns:
        return JSONResponse(
            content={
                "success": True,
                "message": f"成功删除 {deleted_count} 个栏目，{len(failed_columns)} 个栏目无法删除（包含子栏目或关联内容）",
                "count": deleted_count,
                "failed": failed_columns,
            }
        )
    else:
        return JSONResponse(
            content={
                "success": True,
                "message": f"成功删除 {deleted_count} 个栏目",
                "count": deleted_count,
            }
        )
