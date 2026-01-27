"""
留言管理路由
"""

import csv
import io
import math
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from admin.app.database import get_db
from app.models.contact import ContactMessage

router = APIRouter(tags=["contacts"])

templates = Jinja2Templates(directory="admin/templates")


@router.get("", response_class=HTMLResponse)
async def list_contacts(
    request: Request,
    db: Session = Depends(get_db),
    status_filter: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
):
    """
    留言列表页

    支持筛选: status_filter, keyword, page
    """
    # 基础查询
    query = db.query(ContactMessage)

    # 筛选条件
    if status_filter:
        query = query.filter(ContactMessage.status == status_filter)

    if keyword:
        query = query.filter(
            (ContactMessage.name.contains(keyword))
            | (ContactMessage.contact_info.contains(keyword))
            | (ContactMessage.message_text.contains(keyword))
        )

    # 排序: 按创建时间降序
    query = query.order_by(ContactMessage.created_at.desc())

    # 分页
    page_size = 20
    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    # 限制页码范围
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    offset = (page - 1) * page_size
    contacts = query.limit(page_size).offset(offset).all()

    # 统计各状态数量
    unread_count = (
        db.query(ContactMessage).filter(ContactMessage.status == "unread").count()
    )
    handled_count = (
        db.query(ContactMessage).filter(ContactMessage.status == "handled").count()
    )

    return templates.TemplateResponse(
        "contacts/list.html",
        {
            "request": request,
            "contacts": contacts,
            "current_status": status_filter,
            "current_keyword": keyword,
            "page": page,
            "total_pages": total_pages,
            "total": total,
            "unread_count": unread_count,
            "handled_count": handled_count,
        },
    )


@router.get("/{contact_id}", response_class=JSONResponse)
async def get_contact_detail(
    contact_id: int,
    db: Session = Depends(get_db),
):
    """
    获取留言详情 (AJAX)
    """
    contact = db.query(ContactMessage).filter(ContactMessage.id == contact_id).first()

    if not contact:
        raise HTTPException(status_code=404, detail="留言不存在")

    return JSONResponse(
        content={
            "success": True,
            "data": {
                "id": contact.id,
                "name": contact.name,
                "contact_info": contact.contact_info,
                "message_text": contact.message_text,
                "status": contact.status,
                "source_page_url": contact.source_page_url,
                "product_id": contact.product_id,
                "created_at": contact.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "handled_at": (
                    contact.handled_at.strftime("%Y-%m-%d %H:%M:%S")
                    if contact.handled_at
                    else None
                ),
            },
        },
        status_code=status.HTTP_200_OK,
    )


@router.put("/{contact_id}/status", response_class=JSONResponse)
async def update_contact_status(
    contact_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    更新留言状态 (AJAX)

    接收 JSON: {"status": "unread|handled"}
    """
    try:
        # 获取请求体
        body = await request.json()
        new_status = body.get("status")

        if new_status not in ["unread", "handled"]:
            return JSONResponse(
                content={"success": False, "message": "无效的状态"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        contact = (
            db.query(ContactMessage).filter(ContactMessage.id == contact_id).first()
        )

        if not contact:
            raise HTTPException(status_code=404, detail="留言不存在")

        # 更新状态
        contact.status = new_status

        # 如果标记为已处理，记录处理时间
        if new_status == "handled" and not contact.handled_at:
            contact.handled_at = datetime.now()
        # 如果改回未读，清除处理时间
        elif new_status == "unread":
            contact.handled_at = None

        db.commit()

        return JSONResponse(
            content={"success": True, "message": "状态更新成功"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"更新失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/batch/status", response_class=JSONResponse)
async def batch_update_status(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    批量更新留言状态 (AJAX)

    接收 JSON: {"ids": [1, 2, 3], "status": "unread|handled"}
    """
    try:
        body = await request.json()
        ids = body.get("ids", [])
        new_status = body.get("status")

        if not ids:
            return JSONResponse(
                content={"success": False, "message": "未选择留言"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if new_status not in ["unread", "handled"]:
            return JSONResponse(
                content={"success": False, "message": "无效的状态"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 批量更新
        update_data = {"status": new_status}
        if new_status == "handled":
            update_data["handled_at"] = datetime.now()
        elif new_status == "unread":
            update_data["handled_at"] = None

        db.query(ContactMessage).filter(ContactMessage.id.in_(ids)).update(
            update_data, synchronize_session=False
        )
        db.commit()

        return JSONResponse(
            content={"success": True, "message": f"已批量更新 {len(ids)} 条留言"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"批量更新失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.delete("/{contact_id}", response_class=JSONResponse)
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
):
    """
    删除留言
    """
    try:
        contact = (
            db.query(ContactMessage).filter(ContactMessage.id == contact_id).first()
        )

        if not contact:
            raise HTTPException(status_code=404, detail="留言不存在")

        db.delete(contact)
        db.commit()

        return JSONResponse(
            content={"success": True, "message": "留言删除成功"},
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": f"删除失败: {str(e)}"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/export/csv", response_class=StreamingResponse)
async def export_contacts_csv(
    db: Session = Depends(get_db),
    status_filter: Optional[str] = None,
    keyword: Optional[str] = None,
):
    """
    导出留言为 CSV 文件

    支持筛选条件: status_filter, keyword
    """
    # 基础查询
    query = db.query(ContactMessage)

    # 应用相同的筛选条件
    if status_filter:
        query = query.filter(ContactMessage.status == status_filter)

    if keyword:
        query = query.filter(
            (ContactMessage.name.contains(keyword))
            | (ContactMessage.contact_info.contains(keyword))
            | (ContactMessage.message_text.contains(keyword))
        )

    # 排序
    query = query.order_by(ContactMessage.created_at.desc())

    # 获取所有留言
    contacts = query.all()

    # 创建 CSV 内容
    output = io.StringIO()
    writer = csv.writer(output)

    # 写入表头
    headers = [
        "ID",
        "姓名",
        "联系方式",
        "留言内容",
        "状态",
        "来源页面",
        "创建时间",
        "处理时间",
    ]
    writer.writerow(headers)

    # 写入数据
    for contact in contacts:
        status_text = "未读" if contact.status == "unread" else "已处理"
        handled_at_str = (
            contact.handled_at.strftime("%Y-%m-%d %H:%M:%S")
            if contact.handled_at
            else ""
        )
        created_at_str = contact.created_at.strftime("%Y-%m-%d %H:%M:%S")

        writer.writerow(
            [
                contact.id,
                contact.name,
                contact.contact_info,
                contact.message_text,
                status_text,
                contact.source_page_url or "",
                created_at_str,
                handled_at_str,
            ]
        )

    # 准备响应
    output.seek(0)
    response = StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="contacts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        },
    )

    return response
